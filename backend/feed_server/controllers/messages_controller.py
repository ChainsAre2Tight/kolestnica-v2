"""Provides endpoints for message management"""


from flask import Response

from libraries.utils.my_dataclasses import Token
from libraries.utils.http_wrappers import require_access_token, handle_http_exceptions
from libraries.crypto import json_encryptor

from feed_server import app
from feed_server.controllers.interfaces import MessageControllerInterface


class MessageController(MessageControllerInterface):

    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>/messages', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def list_messages(access_token: Token, chat_id: int) -> tuple[Response, int]:
        raise NotImplementedError

    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>/messages/<int:message_id>', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def get_message(access_token: Token, chat_id: int, message_id: int) -> tuple[Response, int]:
        raise NotImplementedError


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>/messages', methods=['POST'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def create_message(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:
        raise NotImplementedError


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>/messages/<int:message_id>', methods=['DELETE'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def delete_message(access_token: Token, chat_id: int, message_id: int) -> tuple[Response, int]:
        raise NotImplementedError


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>/messages/<int:message_id>', methods=['UPDATE'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def update_message(
            access_token: Token,
            chat_id: int,
            message_id: int,
            data: dict
        ) -> tuple[Response, int]:
        raise NotImplementedError
