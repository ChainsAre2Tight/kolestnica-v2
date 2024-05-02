"""Provides API reauests for notification server"""


import requests

from libraries.utils.http_wrappers import require_api_key, handle_http_exceptions

from notification_server import app, api_key
from notification_server.events import ChatEvents, MemberEvents, MessageEvents


def update_sid(session_id: str, sid: str) -> list[int]:
    """Sends a request to authentification server containing socket id and his parent session data

    Args:
        session_id (str): browser fingerprint
        sid (str): socket id of incoming connection

    Returns:
        list[int]: list of chat ids that user has access to
    """
    print('lox', session_id, sid)
    r = requests.patch(
        url='http://nginx/api/users/current/sessions/current',
        headers={'Authorization': api_key},
        json={'socket_id': sid, 'session_id': session_id},
        timeout=10
    )
    assert r.status_code == 200, f'Request of chats failed with HTTP code {r.status_code}.\
 Response: {r.json()}'
    return [int(id_) for id_ in r.json()['data']['chats']]


class ChatRequests:

    @staticmethod
    @app.route('/notifications/chats/', methods=['POST'])
    @require_api_key
    @handle_http_exceptions
    def create_chat(data: dict):
        ChatEvents.create(
            sid=data['sid'],
            chat_id=data['chat_id'],
        )
        return '', 201

    @staticmethod
    @app.route('/notifications/chats/<int:chat_id>', methods=['PATCH'])
    @require_api_key
    @handle_http_exceptions
    def update_chat(_, chat_id: int):
        ChatEvents.update(chat_id=chat_id)
        return '', 200

    @staticmethod
    @app.route('/notifications/chats/<int:chat_id>', methods=['DELETE'])
    @require_api_key
    @handle_http_exceptions
    def delete_chat(_, chat_id: int):
        ChatEvents.delete(chat_id=chat_id)
        return '', 200


class MembersRequests:

    @staticmethod
    @app.route('/notifications/chats/<int:chat_id>/members/', methods=['POST'])
    @require_api_key
    @handle_http_exceptions
    def add_member(data: dict, chat_id: int):
        MemberEvents.add(
            sid=data['sid'],
            chat_id=chat_id
        )
        return '', 201

    @staticmethod
    @app.route('/notifications/chats/<int:chat_id>/members/<str:sid>', methods=['DELETE'])
    @require_api_key
    @handle_http_exceptions
    def remove_member(_, chat_id: int, sid: str):
        MemberEvents.remove(
            sid=sid,
            chat_id=chat_id,
        )
        return '', 200


class MessageRequests:

    @staticmethod
    @app.route('/notifications/chats/<int:chat_id>/messages/', methods=['POST'])
    @require_api_key
    @handle_http_exceptions
    def add_message(data: dict, chat_id: int):
        MessageEvents.add(
            chat_id=chat_id,
            message_id=data['message_id'],
        )
        return '', 201

    @staticmethod
    @app.route('/notifications/chats/<int:chat_id>/messages/<int:message_id>', methods=['DELETE'])
    @require_api_key
    @handle_http_exceptions
    def remove_message(_, chat_id: int, message_id: int):
        MessageEvents.delete(chat_id=chat_id, message_id=message_id)
        return '', 200

    @staticmethod
    @app.route('/notifications/chats/<int:chat_id>/messages/<int:message_id>', methods=['PATCH'])
    @require_api_key
    @handle_http_exceptions
    def add_member(_, chat_id: int, message_id: int):
        MessageEvents.update(chat_id=chat_id, message_id=message_id)
        return '', 200
