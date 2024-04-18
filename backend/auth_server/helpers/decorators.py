


from functools import wraps

from flask import request, jsonify

from auth_server import api_key


def require_api_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            key = dict(request.headers)['Authorization']

            if key != api_key:
                return jsonify({
                    'Ststus': 'Error',
                    'details': 'Wrong API key'
                }), 403
        except KeyError:
            return jsonify({
                    'Ststus': 'Error',
                    'details': 'API key is missing'
                }), 401

        data = request.get_json()
        return func(data, *args, **kwargs)
    return decorated_function
