"""Provides endpoints for chat management"""


from flask import Response, jsonify

from libraries.crypto import json_encryptor
from libraries.utils.http_wrappers import handle_http_exceptions, require_access_token
from libraries.utils.my_dataclasses import Token

from feed_server import app
from feed_server.helpers.quiries_helpers import get_user_id_by_browser_fingerprint
from feed_server.controllers.interfaces import ChatControllerIntarface
from feed_server.services.chats.creator import ChatCreator
from feed_server.services.chats.reader import ChatReader


class ChatController(ChatControllerIntarface):

    @staticmethod
    @app.route('/api/data/chats', methods=['POST'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def get_chats(access_token: Token) -> tuple[Response, int]:
        raise NotImplementedError

    @staticmethod
    @app.route('/api/data/chats', methods=['POST'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def create_chat(access_token: Token, data: dict) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        chat = ChatCreator.create(chat_name=data['name'], user_id=user_id)
        return jsonify(chat.__dict__), 201


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def get_chat_data(access_token: Token, chat_id: int) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        chat = ChatReader.get_chat_data(chat_id=chat_id, user_id=user_id)
        return jsonify(chat.__dict__), 200


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>', methods=['PUT'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def update_chat(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:
        raise NotImplementedError


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>', methods=['DELETE'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def delete_chat(access_token: Token, chat_id: int) -> tuple[Response, int]:
        raise NotImplementedError
