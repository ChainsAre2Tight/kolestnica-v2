"""Provides endpoints for chat members management"""


from flask import Response, jsonify

from libraries.crypto import json_encryptor
from libraries.utils.http_wrappers import handle_http_exceptions, require_access_token
from libraries.utils.my_dataclasses import Token

from feed_server import app
from feed_server.controllers.interfaces import MembersControllerInterface
from feed_server.services.members.adder import MemberAdder
from feed_server.services.members.remover import MemberRemover
from feed_server.services.members.lister import MemberLister
from feed_server.services.members.serializer import MemberSerializer


class MembersController(MembersControllerInterface):

    @staticmethod
    @app.route('/api/chats/<int:chat_id>/members/', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def index_members(access_token: Token, chat_id: int) -> tuple[Response, int]:

        members = MemberLister.list_members(
            chat_id=chat_id,
            browser_fingerprint=access_token.sessionId
        )

        response_data = {
            'Status': 'OK',
            'data': {
                'chat_id': chat_id,
                'members': MemberSerializer.id_name_alias(members=members)
            }
        }
        return jsonify(response_data), 200


    @staticmethod
    @app.route('/api/chats/<int:chat_id>/members/', methods=['POST'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def create_member(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:

        members = MemberAdder.add_member(
            chat_id=chat_id,
            target_id=data['user_id'],
            browser_fingerprint=access_token.sessionId
        )

        response_data = {
            'Status': 'Added',
            'data': {
                'chat_id': chat_id,
                'members': MemberSerializer.to_ids(members=members)
            }
        }
        return jsonify(response_data), 201


    @staticmethod
    @app.route('/api/chats/<int:chat_id>/members/<int:target_id>', methods=['DELETE'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def delete_member(access_token: Token, chat_id: int, target_id: int) -> tuple[Response, int]:

        members = MemberRemover.remove_member(
            chat_id=chat_id,
            target_id=target_id,
            browser_fingerprint=access_token.sessionId
        )

        response_data = {
            'Status': 'Deleted',
            'data': {
                'chat_id': chat_id,
                'members': MemberSerializer.to_ids(members=members)
            }
        }
        return jsonify(response_data), 200
