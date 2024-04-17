"""Provides controller for user management"""


from flask import Response, jsonify

from libraries.utils.my_dataclasses import Token
from libraries.utils.http_wrappers import handle_http_exceptions
from libraries.crypto import json_encryptor

from auth_server import app
from auth_server.controllers.interfaces import UserControllerInterface
from auth_server.services.users.creator import UserCreator


class UserController(UserControllerInterface):

    @staticmethod
    @app.route('/api/auth/users/<int:user_id>', methods=['GET'])
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def show(access_token: Token, user_id: int) -> tuple[Response, int]:
        raise NotImplementedError

    @staticmethod
    @app.route('/api/auth/users/current', methods=['GET'])
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def show_current(access_token: Token) -> tuple[Response, int]:
        raise NotImplementedError


    @staticmethod
    @app.route('/api/auth/users', methods=['POST'])
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def create(data: dict) -> tuple[Response, int]:

        user = UserCreator.create(
            username=data['username'],
            login=data['login'],
            pwdh=data['pwdh']
        )
        response_data = {
            'Status': 'Created',
            'data': {
                'user': user.__dict__
            }
        }
        return jsonify(response_data), 201
