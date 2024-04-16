"""Provides controller for user creation"""

from flask import Response, jsonify

from utils.http_wrappers import handle_http_exceptions

from auth_server.app import app, json_encryptor
from auth_server.controllers.interfaces import UserControllerInterface
from auth_server.actors.users.creator import UserCreator


class UserController(UserControllerInterface):

    @staticmethod
    @app.route('/api/auth/register', methods=['POST'])
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def register_user(credentials: dict) -> tuple[Response, int]:

        user = UserCreator.create(
            username=credentials['username'],
            login=credentials['login'],
            pwdh=credentials['pwdh']
        )
        return jsonify(user.__dict__), 201
