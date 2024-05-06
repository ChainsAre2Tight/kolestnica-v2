


from notification_server import socket
from notification_server.controllers import RoomController


class ChatEvents:

    @staticmethod
    def create(sid, chat_id):
        RoomController.add_user_to_rooms(sid=sid, rooms=[chat_id])

    @staticmethod
    def update(chat_id):
        socket.emit('update-chat', data={'chat_id': chat_id}, to=str(chat_id))

    @staticmethod
    def delete(chat_id):
        socket.emit('drop-chat', data={'chat_id': chat_id}, to=str(chat_id))
        RoomController.remove_room(room=chat_id)


class MemberEvents:

    @staticmethod
    def notify_change(chat_id: int) -> None:
        socket.emit('update-members', data={'chat_id': chat_id}, to=str(chat_id))

    @staticmethod
    def add(sid: str, chat_id: int):
        RoomController.add_user_to_rooms(sid=sid, rooms=[chat_id])
        socket.emit('add-chat', data={'chat_id': chat_id}, to=sid)

    @staticmethod
    def remove(sid: str, chat_id: int):
        RoomController.remove_user_from_rooms(sid=sid, rooms=[chat_id])
        socket.emit('drop-chat', data={'chat_id': chat_id}, to=sid)


class MessageEvents:

    @staticmethod
    def add(chat_id: int, message_id: int):
        print('youve got MALE')
        socket.emit('add-message',
                    data={'chat_id': chat_id, 'message_id': message_id},
                    to=str(chat_id))

    @staticmethod
    def delete(chat_id: int, message_id: int):
        socket.emit('delete-message',
                    data={'chat_id': chat_id, 'message_id': message_id},
                    to=str(chat_id))

    @staticmethod
    def update(chat_id: int, message_id: int):
        socket.emit('update-message',
                    data={'chat_id': chat_id, 'message_id': message_id},
                    to=str(chat_id))
