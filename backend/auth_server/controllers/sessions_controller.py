"""Provides endpoints for session management"""


from flask import make_response, Response, jsonify

from libraries.utils import exc
from libraries.utils.my_dataclasses import Token
from libraries.utils.http_wrappers import handle_http_exceptions, require_access_token
from libraries.crypto import json_encryptor

from auth_server import app
from auth_server.controllers.interfaces import SessionControllerInterface
from auth_server.services.sessions.creator import SessionCreator
from auth_server.services.sessions.deleter import SessionDeleter
from auth_server.services.sessions.updator import SessionUpdator
from auth_server.services.tokens.creator import TokenPairCreator
from auth_server.services.users.reader import UserReader
from auth_server.helpers.request_helpers import provide_access_token, provide_refresh_token
from auth_server.helpers.decorators import require_api_key



class SessionController(SessionControllerInterface):


    @staticmethod
    @app.route('/api/users/current/sessions', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def index_sessions(access_token: Token) -> tuple[Response, int]:
        raise NotImplementedError


    @staticmethod
    @app.route('/api/users/current/sessions', methods=['POST'])
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def create_session(data: dict) -> tuple[Response, int]:
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
                browser_fingerprint=new_session.uuid,
                new_refresh_token=signed_token_pair.refresh
            )

        # construct response
        response_data = provide_access_token(
            {
                'Status': 'Logged in',
                'data': {
                    'User': '!tba!'
                }
            },
            token_pair=signed_token_pair
        )
        response = provide_refresh_token(
            response=make_response(jsonify(response_data)),
            token_pair=signed_token_pair
        )
        return response, 201


    @staticmethod
    @app.route('/api/users/current/sessions/current', methods=['DELETE'])
    @require_access_token
    @handle_http_exceptions
    def delete_current_session(access_token: Token) -> tuple[Response, int]:

        SessionDeleter.delete(browser_fingerprint=access_token.sessionId)
        response_data = {
            'Status': 'Deleted',
            'Details': 'Session successfully terminated'
        }

        response = make_response(jsonify(response_data))
        response.delete_cookie(
            key='r',
            httponly=True,
            path='/api/auth/tokens',
        )
        return response, 200


    @staticmethod
    @require_api_key
    @app.route('/api/users/current/sessions/current', methods=['PATCH'])
    def update_current_session(data: dict) -> tuple[Response, int]:

        SessionUpdator.update_socket_id(
            browser_fingerprint=data['session_id'],
            new_socket_id=data['socket_id']
        )
        chats = UserReader.index_chats(browser_fingerprint=data['session_id'])
        response_data = {
            'Status': 'Updated',
            'data': {
                'chats': chats
            }
        }
        return jsonify(response_data), 200
