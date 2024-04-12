from functools import wraps, partial
from typing import Callable
from flask import request, jsonify
import jwt
import json
import utils.my_exceptions as exc
from flask import Response
import os

from utils.my_dataclasses import Token

TokenPublicKey = os.environ.get('TOKEN-OPEN-KEY') or 'secret'

def require_access_token(
        func: Callable | None=None,
        verify_expiry: bool | None = True
    ) -> tuple[Response, int] | Callable:
    """
    Checks for an access token in the request header and provides its decoded data to decorated function

    :params verify_exp: optional parameter, if set to True skips token expiration check
    :returns:
        decorated function if token verification passes
        HTTP 401 if token signature check failes
        HTTP 403 if token was expired
    """

    if func is None:
        return partial(require_access_token)

    @wraps(func)
    def decorated_function(*args, **kwargs):
        global TokenPublicKey
        try:
            raw_token: str = dict(request.headers)['Authorization']
            token: Token = Token(
                **jwt.decode(
                        raw_token,
                        algorithms=['HS256'],
                        verify=True,
                        key=TokenPublicKey,
                        options={'verify_exp': verify_expiry}
                    )
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