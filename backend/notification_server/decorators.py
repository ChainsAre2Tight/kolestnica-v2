"""Provides sockeio decorators"""

from functools import wraps

import jwt
from flask import request

from libraries.utils.http_wrappers import decode_token

from notification_server import socket

def require_access_token(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            raw_token = kwargs['data']
            access_token = decode_token(raw_token=raw_token)
        except (jwt.DecodeError, jwt.InvalidSignatureError, KeyError):
            socket.emit('bad-token', to=request.sid)
        except jwt.ExpiredSignatureError:
            socket.emit('expired', to=request.sid)
        kwargs['access_token'] = access_token
        return func(*args, **kwargs)
    return decorated_function
