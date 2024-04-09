from flask import jsonify, request, make_response, Response
from utils.wrappers import require_access_token, handle_user_existance
import utils.my_dataclasses as dataclass
import sqlalchemy.exc as sql

from feed.app import app
import feed.queries as q

@app.route('/api/data', methods=['GET'])
@require_access_token
def ping(token) -> tuple[Response, int]:
    """This endpoint provides a way to check service avaliability"""

    return jsonify('pinged'), 200

@app.route('/api/data/chats', methods=['GET'])
@require_access_token
@handle_user_existance
def get_chats(token: dataclass.Token) -> tuple[Response, int]:
    """This endpoint provides a way to get all chats that are accessible to a requesting user"""
    
    chats = dataclass.convert_dataclass_to_dict(
        q.get_chats_by_sessionId(token.sessionId)
    )
    return jsonify(chats), 200

@app.route('/api/data/users', methods=['GET'])
@require_access_token
@handle_user_existance
def get_users(token: dataclass.Token) -> tuple[Response, int]:
    """This endpoint provides a way to get info of users sharing a chat with the issuer"""
    
    users = dataclass.convert_dataclass_to_dict(
        q.get_users_by_sessionId(token.sessionId)
    )
    return jsonify(users), 200

@app.route('/api/data/chats/<int:id>/messages', methods=['GET'])
@require_access_token
@handle_user_existance
def get_messages_by_chat(token: dataclass.Token, id: int) -> tuple[Response, int]:
    """This endpoint provides a way to get all mesages within a specified chat if a user has access to it"""

    messages = dataclass.convert_dataclass_to_dict(
        q.get_messages_by_chat_id(chat_id=id, sessionId=token.sessionId)
    )
    return jsonify(messages), 200