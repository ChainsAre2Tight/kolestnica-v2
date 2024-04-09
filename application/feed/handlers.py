from flask import jsonify, request, make_response, Response
import json
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
    
    chats = [
        chat.__dict__
        for chat in
        q.get_chats_by_sessionId(token.sessionId)
    ]
    return jsonify(chats), 200

@app.route('/api/data/users', methods=['GET'])
@require_access_token
@handle_user_existance
def get_users(token: dataclass.Token) -> tuple[Response, int]:
    """This endpoint provides a way to get info of users sharing a chat with the issuer"""
    
    users = [
        user.__dict__
        for user in
        q.get_users_by_sessionId(token.sessionId)
    ]

    return jsonify(users), 200