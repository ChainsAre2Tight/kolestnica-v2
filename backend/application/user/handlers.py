from flask import Response, make_response, jsonify
import os

from user.app import app
from utils.http_wrappers import require_access_token, handle_http_exceptions, require_refresh_token
import utils.my_dataclasses as dataclass
import user.queries as q
from crypto.json_encryption import JSONEncryptionController
import crypto.encryption_strategies as enc_strat

match os.environ.get('TOKEN_ENCRYPTION_STRATEGY'):
    case 'IDLE':
        encryption = enc_strat.IdleEncryptionStrategy
    case 'REVERSE':
        encryption = enc_strat.ReverseEncryptionStrategy
    case 'CAESAR':
        encryption = enc_strat.CaesarEncryptionStrategy
    case _:
        encryption = enc_strat.IdleEncryptionStrategy

json_controller = JSONEncryptionController(strategy=encryption)

def provide_access_token(response_data: dict, token_pair: dataclass.SignedTokenPair) -> dict:
    """
    `Writes` access and expiry fields into data field of provided response dictionary

    :params dict response_data: dictionary containing necessary response data
    :params SignedTokenPair token_pair: signed token pair dataclass
    :returns: modified response_data dictionary
    """
    if 'data' not in response_data.keys():
        response_data['data'] = dict()
    
    response_data['data']['access'] = token_pair.access
    response_data['data']['expiry'] = token_pair.access_expiry

    return response_data

def provide_refresh_token(response: Response, token_pair: dataclass.SignedTokenPair) -> Response:
    """
    `Adds` a refresh token cookie to response

    :params Response response: Flask Response object
    :params SignedTokenPair token_pair: signed token pair dataclass
    :returns: modified Response object
    """
    
    response.set_cookie(
            key='r',
            value=token_pair.refresh,
            httponly=True,
            path='/auth/refresh',
            expires=token_pair.refresh_expiry
        )
    
    return response

@app.route('/api/auth', methods=['GET'])
@require_access_token
@handle_http_exceptions
def ping(_) -> tuple[Response, int]:
    """This endpoint provides a way to check service avaliability"""

    return jsonify('pinged'), 200

@app.route('/api/auth/register', methods=['POST'])
@handle_http_exceptions
@json_controller.encrypt_json(provide_data=True)
def register_user(data: dict) -> tuple[Response, int]:

    _ = q.create_user(
        data['username'],
        data['login'],
        data['pwdh']
    )

    return jsonify({'Status': 'OK'}), 201

@app.route('/api/auth/login', methods=['POST'])
@handle_http_exceptions
@json_controller.encrypt_json(provide_data=True)
def login_user(data: dict) -> tuple[Response, int]:

    token_pair: dataclass.SignedTokenPair = q.login_user(
        data['login'],
        data['pwdh'],
        data['fingerprint']
    )

    response_data: dict = provide_access_token(
        {
            'status': 'created',
            'data': {}
        },
        token_pair=token_pair
    )

    response = make_response(
        jsonify(response_data)
    )

    response = provide_refresh_token(
        response,
        token_pair=token_pair
    )

    return response, 201

@app.route('/api/auth/logout', methods=['POST'])
@require_access_token
@handle_http_exceptions
def logout_user(token: dataclass.Token) -> tuple[Response, int]:
    """
    This endpoint logs user out of their account and terminates their session
    """

    q.logout_user(token.sessionId)
    payload = {
        'status': 'Deleted',
        'details': 'Session successfully terminated'
    }
    
    response = make_response(jsonify(payload))
    response.delete_cookie(
        key='r',
        httponly=True,
        path='/auth/refresh',
    )

    return response, 200

@app.route('/api/auth/account', methods=['GET'])
@require_access_token
@handle_http_exceptions
@json_controller.encrypt_json()
def view_account_data(token: dataclass.Token) -> tuple[Response, int]:
    """
    This endpoint returns all alivable personal data for the requesting account
    """
    return '', 501


@app.route('/api/auth/account/sessions', methods=['GET'])
@require_access_token
@handle_http_exceptions
@json_controller.encrypt_json()
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

@app.route('/api/auth/refresh-tokens', methods=['POST'])
@require_refresh_token
@handle_http_exceptions
@json_controller.encrypt_json()
def refresh_tokens(
        raw_token: str,
        refresh_token: dataclass.Token,
    ) -> tuple[Response, int]:
    """
    This endpoint provides user with a refreshed token pair upon request
    """

    new_token_pair = q.refresh_tokens(
        raw_token=raw_token,
        refresh=refresh_token
    )

    response_data: dict = provide_access_token(
        {
            'status': 'updated',
            'data': {}
        },
        token_pair=new_token_pair
        )

    response = make_response(
        jsonify(response_data)
    )

    response = provide_refresh_token(
        response,
        token_pair=new_token_pair
    )

    return response, 201
