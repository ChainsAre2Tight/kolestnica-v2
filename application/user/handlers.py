from flask import request, Response, make_response, jsonify

from user.app import app
from utils.wrappers import require_access_token, handle_user_rights
import utils.my_dataclasses as dataclass
import user.queries as q
import utils.my_exceptions as exc

@app.route('/api/auth', methods=['GET'])
@require_access_token
def ping(_) -> tuple[Response, int]:
    """This endpoint provides a way to check service avaliability"""

    return jsonify('pinged'), 200

@app.route('/api/auth/register', methods=['POST'])
def register_user() -> tuple[Response, int]:
    data = request.get_json()

    try:
        _ = q.create_user(
            data['username'],
            data['login'],
            data['pwdh']
        )

        return jsonify({'Status': 'OK'}), 201

    except KeyError:
        return jsonify({'status': 'Error',
            'details': 'Missing data'}), 400
    except exc.DuplicateLoginException:
        return jsonify({'status': 'Error',
            'details': 'An account assosiated with this login already exists'}), 409
    except exc.DuplicateUsernameException:
        return jsonify({'status': 'Error',
            'details': 'This username was already taken by another user'}), 406

@app.route('/api/auth/login', methods=['POST'])
def login_user() -> tuple[Response, int]:
    data = request.get_json()

    try:
        token_pair: dataclass.SignedTokenPair = q.login_user(
            data['login'],
            data['pwdh'],
            data['fingerprint']
        )
        
        response = make_response(
            jsonify({
                'status': 'created',
                'data': {
                    'access': token_pair.access,
                    'expiry': token_pair.access_expiry
                }
            })
        )

        response.set_cookie(
            key='r',
            value=token_pair.refresh,
            httponly=True,
            path='/auth/refresh',
            expires=token_pair.refresh_expiry
        )

        return response, 201
    
    except KeyError:
        return jsonify({
            'status': 'Error',
            'details': 'Missing data'
        }), 400
    except exc.InvalidLoginData:
        return jsonify({
            'status': 'Error',
            'details': "invalid login or password"
        }), 404

@app.route('/api/auth/logout', methods=['POST'])
@require_access_token
@handle_user_rights
def logout_user(token: dataclass.Token) -> tuple[Response, int]:
    """
    This endpoint logs user out of their account and terminates their session
    """
    try:
        q.logout_user(token.sessionId)
        payload, status = {
            'status': 'Deleted',
            'details': 'Session successfully terminated'
        }, 200
    except exc.SessionNotFound:
        payload, status = {
            'Status': 'Gone',
            'details': 'Session was already terminated'
        }, 410
    
    response = make_response(jsonify(payload))
    response.delete_cookie(
        key='r',
        httponly=True,
        path='/auth/refresh',
    )

    return response, status

@app.route('/api/auth/account', methods=['GET'])
@require_access_token
@handle_user_rights
def view_account_data(token: dataclass.Token) -> tuple[Response, int]:
    """
    This endpoint returns all alivable personal data for the requesting account
    """
    return '', 501


@app.route('/api/auth/account/sessions', methods=['GET'])
@require_access_token
@handle_user_rights
def view_sessions(token: dataclass.Token) -> tuple[Response, int]:
    """
    This endpoint lists all active sessions of the requesting account
    """
    sessions = q.list_active_sessions(token.sessionId)
    return jsonify({
        'Status': 'OK',
        'data': {
            'sessions': dataclass.convert_dataclass_to_dict(sessions)
        }
    }), 200
