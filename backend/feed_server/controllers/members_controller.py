"""Provides endpoints for chat members management"""


from flask import Response, jsonify

from libraries.crypto import json_encryptor
from libraries.utils.http_wrappers import handle_http_exceptions, require_access_token
from libraries.utils.my_dataclasses import Token, convert_dataclass_to_dict

from feed_server import app
from feed_server.controllers.interfaces import MembersControllerInterface
from feed_server.helpers.quiries_helpers import get_user_id_by_browser_fingerprint
from feed_server.services.members.adder import MemberAdder
from feed_server.services.members.remover import MemberRemover
from feed_server.services.members.lister import MemberLister


class MembersController(MembersControllerInterface):

    @staticmethod
    @app.route('/api/feed/chats/<int:chat_id>/members', methods=['GET'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def list(access_token: Token, chat_id: int) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        members = MemberLister.list_members(chat_id=chat_id, issuer_id=user_id)

        result = convert_dataclass_to_dict(members)
        return jsonify(result), 200


    @staticmethod
    @app.route('/api/feed/chats/<int:chat_id>/members', methods=['POST'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json(provide_data=True)
    def create(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        members = MemberAdder.add_member(
            chat_id=chat_id,
            issuer_id=user_id,
            target_id=data['user_id']
        )

        result = convert_dataclass_to_dict(members)
        return jsonify(result), 201


    @staticmethod
    @app.route('/api/feed/chats/<int:chat_id>/members/<int:target_id>', methods=['DELETE'])
    @require_access_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def delete(access_token: Token, chat_id: int, target_id: int) -> tuple[Response, int]:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=access_token.sessionId)
        members = MemberRemover.remove_member(
            chat_id=chat_id,
            issuer_id=user_id,
            target_id=target_id
        )

        result = convert_dataclass_to_dict(members)
        return jsonify(result), 200
