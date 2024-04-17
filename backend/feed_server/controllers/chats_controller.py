"""Provides endpoints for chat management"""


from flask import Response, jsonify

from libraries.crypto import json_encryptor
from libraries.utils.http_wrappers import handle_http_exceptions, require_access_token
from libraries.utils.my_dataclasses import Token, convert_dataclass_to_dict

from feed_server import app
from feed_server.helpers.quiries_helpers import get_user_id_by_browser_fingerprint
from feed_server.controllers.interfaces import ChatControllerIntarface
from feed_server.services.chats.creator import ChatCreator
from feed_server.services.chats.reader import ChatReader


class ChatController(ChatControllerIntarface):

    @staticmethod
    @app.route('/api/data/chats', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def index(access_token: Token) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        chats = ChatReader.get_chats(user_id=user_id)
        chast_data = convert_dataclass_to_dict(chats)

        response_data = {
            'Status': 'OK',
            'data': {
                'chats': chast_data
            }
        }
        return jsonify(response_data), 200


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def show(access_token: Token, chat_id: int) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        chat = ChatReader.get_chat_data(chat_id=chat_id, user_id=user_id)

        response_data = {
            'Status': 'OK',
            'data': {
                'chat': chat.__dict__
            }
        }
        return jsonify(response_data), 200


    @staticmethod
    @app.route('/api/data/chats', methods=['POST'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def create(access_token: Token, data: dict) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        chat = ChatCreator.create(chat_name=data['name'], user_id=user_id)

        response_data = {
            'Status': 'Created',
            'data': {
                'chat': chat.__dict__
            }
        }
        return jsonify(response_data), 201


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>', methods=['PATCH'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def update(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:
        raise NotImplementedError


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>', methods=['DELETE'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def delete(access_token: Token, chat_id: int) -> tuple[Response, int]:
        raise NotImplementedError
