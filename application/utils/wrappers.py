from functools import wraps
from flask import request, jsonify
import jwt
import json
from sqlalchemy.exc import NoResultFound
from utils.my_exceptions import NoAcccessException

from utils.my_dataclasses import Token

def require_access_token(func):
    """Provides an interface to check for access token provided in a request and access its data"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            raw_token: str = dict(request.headers)['Authorization']
            token: Token = Token(
                **jwt.decode(raw_token, algorithms=['HS256'], verify=True, key='secret')
                )
        except (KeyError, json.JSONDecodeError): #TODO remove this in production
            return jsonify({'Error': 'Missing access token'}), 400
        except (jwt.DecodeError, jwt.InvalidSignatureError):
            return jsonify({'Error': 'Bad access token'}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({'Error': 'Expired access token'}), 401
        
        return func(token, *args, **kwargs)
    
    return decorated_function

def handle_user_rights(func):
    """Handles an instance when session that sent the request was terminated that returns a HTTP 401"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoResultFound:
            return jsonify({"Error": "User doesn't exist"}), 401
        except NoAcccessException:
            return jsonify({'Error': 'Cannot access requested data'}), 403
    
    return decorated_function