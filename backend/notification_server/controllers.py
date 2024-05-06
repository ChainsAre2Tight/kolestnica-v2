"""Provides controllers"""


from flask import request
from flask_socketio import join_room, leave_room, disconnect
import jwt

from libraries.utils.http_wrappers import decode_token

from notification_server import socket
from notification_server.api import update_sid


class EventController:

    @staticmethod
    @socket.on('connect')
    def handle_connection(data):
        raw_token = request.args.get('access_token')
        print('!!! -->', request.sid)
        try:
            access_token = decode_token(raw_token=raw_token)
            print(access_token)
        except (jwt.DecodeError, jwt.InvalidSignatureError, KeyError):
            socket.emit('bad-token', to=request.sid)
            disconnect(request.sid)
        except jwt.ExpiredSignatureError:
            socket.emit('expired', to=request.sid)
            disconnect(request.sid)
        else:
            chats = update_sid(session_id=access_token.sessionId, sid=request.sid)
            RoomController.add_user_to_rooms(sid=request.sid, rooms=chats)

class RoomController:

    @staticmethod
    def remove_room(room):
        socket.close_room(room=room)

    @staticmethod
    def add_user_to_rooms(sid: str, rooms: list[int]):
        for room in rooms:
            print(f'--> added {sid} to {room}')
            join_room(room=str(room), sid=sid, namespace='/')

    @staticmethod
    def remove_user_from_rooms(sid: str, rooms: list[int]):
        for room in rooms:
            leave_room(room=str(room), sid=sid, namespace='/')
