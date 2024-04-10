from flask import jsonify, request, make_response, Response

from utils.wrappers import require_access_token, handle_user_rights
import utils.my_dataclasses as dataclass
from feed.app import app
import feed.queries as q

@app.route('/api/data', methods=['GET'])
@require_access_token
def ping(_) -> tuple[Response, int]:
    """This endpoint provides a way to check service avaliability"""

    return jsonify('pinged'), 200

@app.route('/api/data/chats', methods=['GET'])
@require_access_token
@handle_user_rights
def get_chats(token: dataclass.Token) -> tuple[Response, int]:
    """
    This endpoint provides a way to get all chats\
    that are accessible to a requesting user
    """
    
    chats = dataclass.convert_dataclass_to_dict(
        q.get_chats_by_sessionId(token.sessionId)
    )
    return jsonify(chats), 200

@app.route('/api/data/users', methods=['GET'])
@require_access_token
@handle_user_rights
def get_users(token: dataclass.Token) -> tuple[Response, int]:
    """
    This endpoint provides a way to get info of users\
    sharing a chat with the issuer
    """
    
    users = dataclass.convert_dataclass_to_dict(
        q.get_users_by_sessionId(token.sessionId)
    )
    return jsonify(users), 200

@app.route('/api/data/chats/<int:c_id>/messages', methods=['GET'])
@require_access_token
@handle_user_rights
def get_messages_by_chat(token: dataclass.Token, c_id: int) -> tuple[Response, int]:
    """
    This endpoint provides a way to get all mesages \
    within a specified chat if a user has access to it
    """

    messages = dataclass.convert_dataclass_to_dict(
        q.get_messages_by_chat_id(chat_id=c_id, sessionId=token.sessionId)
    )
    return jsonify(messages), 200

@app.route('/api/data/chats/<int:c_id>/messages', methods=['POST'])
@require_access_token
@handle_user_rights
def send_message(token: dataclass.Token, c_id: int) -> tuple[Response, int]:
    """
    This endpoint serves to provide a way to send new messages\
        to database and notify all clients that can access it
    """
    data = request.get_json()
    # construct dataclass object
    raw_message = dataclass.Message(
        id=None,
        body=data['body'],
        timestamp=data['timestamp'],
        chat_id=c_id,
        author_id=None
    )
    # send to database and fill missing message data
    processesed_message = q.store_message(
        sessionId=token.sessionId,
        message=raw_message
    )
    # if successful, send message data to notification server
    pass # TODO send data to notification server

    # return success to user
    return jsonify(processesed_message.__dict__), 201