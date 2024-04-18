"""Provides controllers"""


from flask import request
from flask_socketio import join_room, leave_room
import jwt

from libraries.utils.my_dataclasses import Token
from libraries.utils.http_wrappers import decode_token

from notification_server import socket
from notification_server.api import update_sid


class EventController:

    @staticmethod
    @socket.on('connection')
    def handle_connection(data: dict, access_token: Token):
        try:
            access_token = decode_token(raw_token=data['data'])
        except (jwt.DecodeError, jwt.InvalidSignatureError, KeyError):
            socket.emit('bad-token', to=request.sid)
        except jwt.ExpiredSignatureError:
            socket.emit('expired', to=request.sid)
        chats = update_sid(session_id=access_token.sessionId, sid=request.sid)
        RoomController.add_user_to_rooms(sid=request.sid, rooms=chats)


class RoomController:

    @staticmethod
    def remove_room(room):
        socket.close_room(room=room)

    @staticmethod
    def add_user_to_rooms(sid: str, rooms: list[int]):
        for room in rooms:
            join_room(room=room, sid=sid)

    @staticmethod
    def remove_user_from_rooms(sid: str, rooms: list[int]):
        for room in rooms:
            leave_room(room=room, sid=sid)
