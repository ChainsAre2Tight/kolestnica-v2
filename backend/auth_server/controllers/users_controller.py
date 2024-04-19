"""Provides controller for user management"""


from flask import Response, jsonify

from libraries.utils.my_dataclasses import Token
from libraries.utils.http_wrappers import handle_http_exceptions, require_access_token
from libraries.crypto import json_encryptor

from auth_server import app
from auth_server.controllers.interfaces import UserControllerInterface
from auth_server.services.users.creator import UserCreator
from auth_server.services.users.reader import UserReader
from auth_server.services.users.serializer import UserSerializer


class UserController(UserControllerInterface):

    @staticmethod
    @app.route('/api/users/<int:user_id>', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def show_user(access_token: Token, user_id: int) -> tuple[Response, int]:
        raise NotImplementedError

    @staticmethod
    @app.route('/api/users/current', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def show_current_user(access_token: Token) -> tuple[Response, int]:
        user = UserReader.show_current(browser_fingerprint=access_token.sessionId)
        response_data = {
            'Status': 'OK',
            'data': {
                'User': UserSerializer.full(user=user)
            }
        }
        return jsonify(response_data), 200

    @staticmethod
    @app.route('/api/users/', methods=['POST'])
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def create_user(data: dict) -> tuple[Response, int]:

        user = UserCreator.create(
            username=data['username'],
            login=data['login'],
            pwdh=data['pwdh']
        )
        response_data = {
            'Status': 'Created',
            'data': {
                'user': UserSerializer.full(user=user)
            }
        }
        return jsonify(response_data), 201
