"""This module contains wrappers for Flask request handlers"""

from functools import wraps, partial
from typing import Callable
from flask import request, jsonify
import jwt
import json
import utils.exc as exc
from flask import Response, make_response


from utils.my_dataclasses import Token

def decode_token(raw_token: str) -> Token:
    return Token(**jwt.decode(
        jwt=raw_token,
        key='secret',
        algorithms=['HS256']
    ))


def require_access_token(func: Callable) -> tuple[Response, int] | Callable:
    """
    Checks for an access token in the request header and provides its decoded data to decorated function

    :returns:
        decorated function: if token verification passes
        HTTP 401: if token signature check failes
        HTTP 403: if token was expired
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            raw_token: str = dict(request.headers)['Authorization']
            token: Token = decode_token(raw_token=raw_token)
        
        except (jwt.DecodeError, jwt.InvalidSignatureError, KeyError, json.JSONDecodeError):
            return jsonify({
                'Staus': 'Error',
                'details': 'Access token is missing or is invalid'
            }), 401
        except jwt.ExpiredSignatureError:
            return jsonify({
                'Staus': 'Error',
                'details': 'Access token is expired'
            }), 403
        
        return func(token, *args, **kwargs)
    
    return decorated_function

def require_refresh_token(func: Callable | None=None) -> tuple[Response, int] | Callable:
    """
    Checks for a refresh token in the request cookies and provides \
        both its raw and decoded data to decorated function

    :returns:
        decorated function: if token verification passes
        HTTP 401: if token signature check failes
        HTTP 403: if token was expired
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):

        try:
            raw_token: str = request.cookies['r']
            decoded_token: Token = decode_token(raw_token=raw_token)
        
        except (jwt.DecodeError, jwt.InvalidSignatureError, KeyError, json.JSONDecodeError):
            return jsonify({
                'Staus': 'Error',
                'details': 'Refresh token is missing or is invalid'
            }), 401
        except jwt.ExpiredSignatureError:
            return jsonify({
                'Staus': 'Error',
                'details': 'Refresh token is expired'
            }), 403
        
        return func(raw_token, decoded_token, *args, **kwargs)
    
    return decorated_function

def handle_http_exceptions(
            func: Callable | None = None,
            options: dict=None
        ) -> Callable | tuple[Response, int]:
    """
    Handles exception related to user access rights and returns HTTP error responses
    """

    if func is None:
        return partial(handle_http_exceptions)
    
    def make_err_response(
            description: str,
            error: Exception
        ) -> Response:

        try:
            details = error.args[0]
        except IndexError:
            details = 'No details provided'

        return make_response(
            jsonify({
                'Status': 'Error',
                'Error': description,
                'Details': details
            })
        )
    
    @wraps(func)
    def decorated_function(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        
        except KeyError as e:
            return make_err_response('Missing data', e), 400
        except exc.UserNotExistsException as e:
            return make_err_response("Bad session data", e), 401
        except exc.NoAcccessException as e:
            return make_err_response('Cannot access requested data', e), 404
        except exc.NotPermittedException as e:
            return make_err_response("Action is prohibited", e), 403
        except exc.UserNotFoundException as e:
            return make_err_response('Requested user does not exist', e), 404
        except exc.RequestAlreadyFullfilledException as e:
            return make_err_response("Requirement is already fullfilled", e), 406
        except exc.DeprecatedRefreshToken as e:
            return make_err_response("Refresk token is invalid or has expired", e), 401
        except exc.DuplicateLoginException as e:
            return make_err_response('An account assosiated with this login already exists', e), 409
        except exc.DuplicateUsernameException as e:
            return make_err_response('This username was already taken by another user', e), 406
        except exc.InvalidLoginData as e:
            return make_err_response('Invalid login or password', e), 404
        except exc.SessionNotFound as e:
            return make_err_response('Session was already terminated or didnt exist in the first place', e), 410
        except exc.BadEncryptionKeys as e:
            return make_err_response('Missing encryption keys', e), 401
    
    return decorated_function