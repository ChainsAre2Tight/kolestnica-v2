"""Provides endpoints for session management"""

from flask import make_response, Response, jsonify

from utils import exc
from utils.my_dataclasses import Token
from utils.http_wrappers import handle_http_exceptions, require_access_token

from auth_server import app, json_encryptor

from auth_server.controllers.interfaces import SessionControllerInterface
from auth_server.services.sessions.creator import SessionCreator
from auth_server.services.sessions.deleter import SessionDeleter
from auth_server.services.sessions.updator import SessionUpdator
from auth_server.services.tokens.creator import TokenPairCreator
from auth_server.helpers.request_helpers import provide_access_token, provide_refresh_token


class SessionController(SessionControllerInterface):

    @staticmethod
    @app.route('/api/auth/login', methods=['POST'])
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def login_user(data: dict) -> tuple[Response, int]:
        try:
            new_session = SessionCreator.create(
                login=data['login'],
                pwdh=data['pwdh'],
                browser_fingerprint=data['fingerprint']
            )
        except exc.AlreadyLoggedIn:
            SessionDeleter.delete(browser_fingerprint=data['fingerprint'])
        new_session = SessionCreator.create(
                login=data['login'],
                pwdh=data['pwdh'],
                browser_fingerprint=data['fingerprint']
            )

        signed_token_pair = TokenPairCreator.create(browser_fingerprint=data['fingerprint'])

        SessionUpdator.update_refresh_token(
                session_id=new_session.id,
                new_refresh_token=signed_token_pair.refresh
            )

        # construct response
        response_data = provide_access_token(
            {'Status': 'Logged in', 'data': {}},
            token_pair=signed_token_pair
        )
        response = provide_refresh_token(
            response=make_response(jsonify(response_data)),
            token_pair=signed_token_pair
        )
        return response, 201


    @staticmethod
    @app.route('/api/auth/logout', methods=['POST'])
    @require_access_token
    def logout(access_token: Token) -> tuple[Response, int]:

        SessionDeleter.delete(browser_fingerprint=access_token.sessionId)
        payload = {
            'Status': 'Deleted',
            'Details': 'Session successfully terminated'
        }

        response = make_response(jsonify(payload))
        response.delete_cookie(
            key='r',
            httponly=True,
            path='/auth/refresh',
        )
        return response, 200


    @staticmethod
    @app.route('/api/auth/account/sessions', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def list_sessions(access_token: Token) -> tuple[Response, int]:
        raise NotImplementedError
