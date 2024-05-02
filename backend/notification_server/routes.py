


from libraries.utils.http_wrappers import require_api_key, handle_http_exceptions

from notification_server import app
from notification_server.events import ChatEvents, MemberEvents, MessageEvents


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
    @app.route('/notifications/chats/<int:chat_id>/members/<sid>', methods=['DELETE'])
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
    def update_message(_, chat_id: int, message_id: int):
        MessageEvents.update(chat_id=chat_id, message_id=message_id)
        return '', 200
