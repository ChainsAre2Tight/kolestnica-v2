"""Provides controller for user creation"""

from flask import Response, jsonify

from libraries.utils.http_wrappers import handle_http_exceptions
from libraries.crypto import json_encryptor

from auth_server import app
from auth_server.controllers.interfaces import UserControllerInterface
from auth_server.services.users.creator import UserCreator


class UserController(UserControllerInterface):

    @staticmethod
    @app.route('/api/auth/register', methods=['POST'])
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def register_user(data: dict) -> tuple[Response, int]:

        user = UserCreator.create(
            username=data['username'],
            login=data['login'],
            pwdh=data['pwdh']
        )
        return jsonify(user.__dict__), 201
