"""Provides endpoints for message management"""


from flask import Response, jsonify

from libraries.utils.my_dataclasses import Token, convert_dataclass_to_dict
from libraries.utils.http_wrappers import require_access_token, handle_http_exceptions
from libraries.crypto import json_encryptor

from feed_server import app
from feed_server.controllers.interfaces import MessageControllerInterface
from feed_server.helpers.quiries_helpers import get_user_id_by_browser_fingerprint
from feed_server.services.messages.getter import MessageGetter
from feed_server.services.messages.creator import MessageCreator
from feed_server.services.messages.updater import MessageUpdater
from feed_server.services.messages.deleter import MessageDeleter


class MessageController(MessageControllerInterface):

    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>/messages', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def index(access_token: Token, chat_id: int) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        messages = MessageGetter.list_messages(user_id=user_id, chat_id=chat_id)

        messages_data = convert_dataclass_to_dict(messages)
        response_data = {
            'Status': 'OK',
            'data': {
                'messages': messages_data
            }
        }
        return jsonify(response_data), 200

    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>/messages/<int:message_id>', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def show(access_token: Token, chat_id: int, message_id: int) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        message = MessageGetter.get_message(user_id=user_id, chat_id=chat_id, message_id=message_id)

        response_data = {
            'Status': 'OK',
            'data': {
                'messages': message.__dict__
            }
        }
        return jsonify(response_data), 200


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>/messages', methods=['POST'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def create(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        message_id = MessageCreator.create_message(
            user_id=user_id,
            chat_id=chat_id,
            text=data['message']['body'],
            timestamp=data['message']['timestamp']
        )

        response_data = {
            'Status': 'Created',
            'data': {
                'message': {
                    'id': message_id
                }
            }
        }
        return jsonify(response_data), 201


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>/messages/<int:message_id>', methods=['PATCH'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def update_message(
            access_token: Token,
            chat_id: int,
            message_id: int,
            data: dict
        ) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        message_id = MessageUpdater.update_body(
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            new_body=data['message']['body']
        )

        response_data = {
            'Status': 'Updated',
            'data': {
                'message': {
                    'id': message_id
                }
            }
        }
        return jsonify(response_data), 200


    @staticmethod
    @app.route('/api/data/chats/<int:chat_id>/messages/<int:message_id>', methods=['DELETE'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def delete(access_token: Token, chat_id: int, message_id: int) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        message_id = MessageDeleter.delete_message(
            user_id=user_id,
            chat_id=chat_id, 
            message_id=message_id
        )

        response_data = {
            'Status': 'Deleted',
            'data': {
                'message': {
                    'id': message_id
                }
            }
        }
        return jsonify(response_data), 200
