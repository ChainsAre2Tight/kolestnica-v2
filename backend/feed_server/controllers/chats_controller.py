"""Provides endpoints for chat management"""


from flask import Response, jsonify

from libraries.crypto import json_encryptor
from libraries.utils.my_dataclasses import Token
from libraries.utils.http_wrappers import handle_http_exceptions, require_access_token

from feed_server import app
from feed_server.controllers.interfaces import ChatControllerIntarface
from feed_server.services.chats.creator import ChatCreator
from feed_server.services.chats.reader import ChatReader
from feed_server.services.chats.serializer import ChatSerializer
from feed_server.services.chats.patcher import ChatPatcher


class ChatController(ChatControllerIntarface):

    @staticmethod
    @app.route('/api/chats/', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def index_chats(access_token: Token) -> tuple[Response, int]:

        chats = ChatReader.get_chats(browser_fingerprint=access_token.sessionId)

        response_data = {
            'Status': 'OK',
            'data': {
                'chats': ChatSerializer.to_ids(chats=chats)
            }
        }
        return jsonify(response_data), 200


    @staticmethod
    @app.route('/api/chats/<int:chat_id>', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def show_chat(access_token: Token, chat_id: int) -> tuple[Response, int]:

        chat = ChatReader.get_chat_data(chat_id=chat_id, browser_fingerprint=access_token.sessionId)
        response_data = {
            'Status': 'OK',
            'data': {
                'chat': ChatSerializer.full(chat=chat)
            }
        }
        return jsonify(response_data), 200


    @staticmethod
    @app.route('/api/chats/', methods=['POST'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def create_chat(access_token: Token, data: dict) -> tuple[Response, int]:

        chat = ChatCreator.create(
            chat_name=data['name'],
            chat_image_href=data['image_href'],
            browser_fingerprint=access_token.sessionId
        )
        response_data = {
            'Status': 'Created',
            'data': {
                'chat': ChatSerializer.full(chat=chat)
            }
        }
        return jsonify(response_data), 201


    @staticmethod
    @app.route('/api/chats/<int:chat_id>', methods=['PATCH'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def update_chat(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:

        chat = ChatPatcher.update_image(
            browser_fingerprint=access_token.sessionId,
            chat_id=chat_id,
            image_href=data['image_href']
        )
        response_data = {
            'Status': 'Updated',
            'data': {
                'chat': ChatSerializer.full(chat=chat)
            }
        }
        return jsonify(response_data), 200


    @staticmethod
    @app.route('/api/chats/<int:chat_id>', methods=['DELETE'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def delete_chat(access_token: Token, chat_id: int) -> tuple[Response, int]:
        raise NotImplementedError
