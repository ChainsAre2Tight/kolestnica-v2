from functools import wraps, partial
from typing import Callable
from flask import request, jsonify
import jwt
import json
import utils.my_exceptions as exc
from flask import Response
import os
from typing_extensions import Literal

from utils.my_dataclasses import Token

TokenPublicKey = os.environ.get('TOKEN-PUBLIC-KEY') or 'secret'

def decode_token(
        raw_token: str,
        algorithm: Literal['HS256', 'RS256'] = 'HS256',
        verify_expiration: bool = True
    ) -> Token:
    """
    Decodes a token

    :params:
        str raw_token: string containing JWT token
        str algorithm: signature algorithm
        bool verify_expiration: if set to False will skip expiration check
    
    :returns dataclass.Token: dataclass Token object containing decoded token data
    """
    return Token(
        **jwt.decode(
            raw_token,
            algorithms=[algorithm],
            options={'verify_exp': verify_expiration},
            key=TokenPublicKey
        )
    )

def require_access_token(
        func: Callable | None=None,
        verify_expiry: bool | None = True
    ) -> tuple[Response, int] | Callable:
    """
    Checks for an access token in the request header and provides its decoded data to decorated function

    :params verify_exp: optional parameter, if set to True skips token expiration check
    :returns:
        decorated function: if token verification passes
        HTTP 401: if token signature check failes
        HTTP 403: if token was expired
    """

    if func is None:
        return partial(require_access_token)

    @wraps(func)
    def decorated_function(*args, **kwargs):
        global TokenPublicKey
        try:
            raw_token: str = dict(request.headers)['Authorization']
            token: Token = decode_token(
                raw_token=raw_token,
                algorithm='HS256',
                verify_expiration=verify_expiry
            )
        
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

def require_refresh_token(
        func: Callable | None=None,
    ) -> tuple[Response, int] | Callable:
    """
    Checks for a refresh token in the request cookies and provides \
        both its raw and decoded data to decorated function

    :returns:
        decorated function: if token verification passes
        HTTP 401: if token signature check failes
        HTTP 403: if token was expired
    """

    if func is None:
        return partial(require_access_token)

    @wraps(func)
    def decorated_function(*args, **kwargs):
        global TokenPublicKey
        try:
            raw_token: str = request.cookies['r']
            decoded_token: Token = decode_token(
                raw_token=raw_token,
                algorithm='HS256'
            )
        
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

def handle_user_rights(func):
    """Handles exception related to user access rights and returns HTTP error responses"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return jsonify({'Error': 'Missing data'}), 400
        except exc.UserNotExistsException:
            return jsonify({"Error": "Bad session data"}), 401
        except exc.NoAcccessException:
            return jsonify({'Error': 'Cannot access requested data'}), 404
        except exc.NotPermittedException:
            return jsonify({'Error': "Action is prohibited"}), 403
        except exc.UserNotFoundException:
            return jsonify({'Error': 'Requested user does not exist'}), 404
        except exc.RequestAlreadyFullfilledException:
            return jsonify({'Error': "Requirement is already fullfilled"}), 406
    
    return decorated_function