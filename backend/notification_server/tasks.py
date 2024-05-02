"""Provides tasks for notification server"""


from notification_server import socket, celery
from notification_server.controllers import RoomController


# chats
@celery.task(name='create_chat')
def create_chat(sid: str, chat_id: int):
    RoomController.add_user_to_rooms(sid=sid, rooms=[chat_id])

@celery.task(name='update_chat')
def update_chat(chat_id: int):  # Unused as it lacks interactor
    socket.emit('update-chat', data={'chat_id': chat_id}, to=chat_id)

@celery.task(name='delete_chat')
def delete_chat(chat_id: int):  # Unused as it lacks interactor
    socket.emit('drop-chat', data={'chat_id': chat_id}, to=chat_id)
    RoomController.remove_room(room=chat_id)



# members
@celery.task(name='add_to_chat')
def add_to_chat(sid: str, chat_id: int):
    RoomController.add_user_to_rooms(sid=sid, rooms=[chat_id])
    socket.emit('add-chat', data={'chat_id': chat_id}, to=sid)

@celery.task(name='remove_from_chat')
def remove_from_chat(sid: str, chat_id: int):
    RoomController.remove_user_from_rooms(sid=sid, rooms=[chat_id])
    socket.emit('drop-chat', data={'chat_id': chat_id}, to=sid)



# messages
@celery.task(name='add_message')
def add_message(chat_id: int, message_id: int):
    print('youve got MALE')
    print('??? celery socket is', socket)
    socket.emit('add-message', data={'chat_id': chat_id, 'message_id': message_id}, to='37')

@celery.task(name='delete_message')
def delete_message(chat_id: int, message_id: int):
    socket.emit('delete-message', data={'chat_id': chat_id, 'message_id': message_id}, to=chat_id)

@celery.task(name='update_message')
def update_message(chat_id: int, message_id: int):
    socket.emit('update-message', data={'chat_id': chat_id, 'message_id': message_id}, to=chat_id)
