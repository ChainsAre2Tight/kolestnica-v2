"""Provides endpoints for message management"""


from flask import Response, jsonify

from libraries.utils.my_dataclasses import Token
from libraries.utils.http_wrappers import require_access_token, handle_http_exceptions
from libraries.crypto import json_encryptor

from feed_server import app
from feed_server.controllers.interfaces import MessageControllerInterface
from feed_server.services.messages.getter import MessageGetter
from feed_server.services.messages.creator import MessageCreator
from feed_server.services.messages.updater import MessageUpdater
from feed_server.services.messages.deleter import MessageDeleter
from feed_server.services.messages.serializer import MessageSerializer


class MessageController(MessageControllerInterface):

    @staticmethod
    @app.route('/api/chats/<int:chat_id>/messages/', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def index_messages(access_token: Token, chat_id: int) -> tuple[Response, int]:

        messages = MessageGetter.list_messages(
            chat_id=chat_id,
            browser_fingerprint=access_token.sessionId
        )
        response_data = {
            'Status': 'OK',
            'data': {
                'chat_id': chat_id,
                'messages': MessageSerializer.full_list(messages=messages)
            }
        }
        return jsonify(response_data), 200

    @staticmethod
    @app.route('/api/chats/<int:chat_id>/messages/<int:message_id>', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def show_message(access_token: Token, chat_id: int, message_id: int) -> tuple[Response, int]:

        message = MessageGetter.get_message(
            chat_id=chat_id,
            message_id=message_id,
            browser_fingerprint=access_token.sessionId
        )
        response_data = {
            'Status': 'OK',
            'data': {
                'chat_id': chat_id,
                'message': MessageSerializer.full(message=message)
            }
        }
        return jsonify(response_data), 200


    @staticmethod
    @app.route('/api/chats/<int:chat_id>/messages/', methods=['POST'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def create_message(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:

        message = MessageCreator.create_message(
            browser_fingerprint=access_token.sessionId,
            chat_id=chat_id,
            text=data['message']['body'],
            timestamp=data['message']['timestamp']
        )
        response_data = {
            'Status': 'Created',
            'data': {
                'chat_id': chat_id,
                'message_id': MessageSerializer.to_id(message=message) 
            }
        }
        return jsonify(response_data), 201


    @staticmethod
    @app.route('/api/chats/<int:chat_id>/messages/<int:message_id>', methods=['PATCH'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def update_message(
            access_token: Token,
            chat_id: int,
            message_id: int,
            data: dict
        ) -> tuple[Response, int]:

        message = MessageUpdater.update_body(
            browser_fingerprint=access_token.sessionId,
            chat_id=chat_id,
            message_id=message_id,
            new_body=data['message']['body']
        )
        response_data = {
            'Status': 'Updated',
            'data': {
                'chat_id': chat_id,
                'message_id': MessageSerializer.to_id(message=message)
            }
        }
        return jsonify(response_data), 200


    @staticmethod
    @app.route('/api/chats/<int:chat_id>/messages/<int:message_id>', methods=['DELETE'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def delete_message(access_token: Token, chat_id: int, message_id: int) -> tuple[Response, int]:

        message = MessageDeleter.delete_message(
            browser_fingerprint=access_token.sessionId,
            chat_id=chat_id, 
            message_id=message_id
        )
        response_data = {
            'Status': 'Deleted',
            'data': {
                'chat_id': chat_id,
                'message_id': MessageSerializer.to_id(message=message)
            }
        }
        return jsonify(response_data), 200
