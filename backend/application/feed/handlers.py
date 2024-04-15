from flask import jsonify, request, Response

from utils.http_wrappers import require_access_token, handle_http_exceptions
import utils.my_dataclasses as dataclass
from feed.app import app
import feed.queries as q
from crypto.json_encryption import JSONEncryptionController

json_controller = JSONEncryptionController.build()

@app.route('/api/data', methods=['GET'])
@require_access_token
def ping(_) -> tuple[Response, int]:
    """This endpoint provides a way to check service avaliability"""

    return jsonify('pinged'), 200

@app.route('/api/data/chats', methods=['GET'])
@require_access_token
@handle_http_exceptions
@json_controller.encrypt_json()
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
@handle_http_exceptions
@json_controller.encrypt_json()
def get_users(token: dataclass.Token) -> tuple[Response, int]:
    """
    This endpoint provides a way to get info of users\
    sharing a chat with the issuer
    """
    
    users = dataclass.convert_dataclass_to_dict(
        q.get_users_by_sessionId(token.sessionId)
    )
    return jsonify(users), 200

@app.route('/api/data/chats/<int:c_id>/users', methods=['GET'])
@require_access_token
@handle_http_exceptions
@json_controller.encrypt_json()
def get_users_by_chat(token: dataclass.Token, c_id: int) -> tuple[Response, int]:
    """
    This endpoint provides a way to yield all users of a certain chat if user has access to it
    """
    users = dataclass.convert_dataclass_to_dict(
        q.get_users_of_certain_chat(token.sessionId, c_id)
    )
    return jsonify(users), 200

@app.route('/api/data/chats/<int:c_id>/users', methods=['POST'])
@require_access_token
@handle_http_exceptions
@json_controller.encrypt_json(provide_data=True)
def add_user_to_chat(token: dataclass.Token, c_id: int, data: dict) -> tuple[Response, int]:
    """
    This endpoint lets user add other users to the chat
    """
    user = q.add_user_to_chat(
        sessionId=token.sessionId,
        chat_id=c_id,
        username=data['username']
    )

    return jsonify(user.__dict__), 201


@app.route('/api/data/chats/<int:c_id>/messages', methods=['GET'])
@require_access_token
@handle_http_exceptions
@json_controller.encrypt_json()
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
@handle_http_exceptions
@json_controller.encrypt_json(provide_data=True)
def send_message(token: dataclass.Token, c_id: int, data: dict) -> tuple[Response, int]:
    """
    This endpoint serves to provide a way to send new messages\
        to database and notify all clients that can access it
    """
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
    return jsonify({
        'msg_id': processesed_message.id
    }), 201

@app.route('/api/data/chats/<int:c_id>/messages/<int:m_id>', methods=['DELETE'])
@require_access_token
@handle_http_exceptions
@json_controller.encrypt_json()
def delete_message(token: dataclass.Token, c_id: int, m_id: int) -> tuple[Response, int]:
    """
    This endpoint provides a way to delete message by its author
    """
    # try to delete message
    msg_to_delete = q.delete_message(sessionId=token.sessionId, chat_id=c_id, message_id=m_id)

    # if successfull, send message data to notification server
    pass # TODO send data to notification server

    # return success tu user
    return jsonify({'msg_id': msg_to_delete['msg_id']}), 200

@app.route('/api/data/chats', methods=['POST'])
@require_access_token
@handle_http_exceptions
@json_controller.encrypt_json()
def create_chat(token: dataclass.Token) -> tuple[Response, int]:
    """
    This endpoint provides a mean to create a new chat
    """
    # get chat data from user
    data = request.get_json()

    # store it into database
    chat = q.create_chat(sessionId=token.sessionId, chat_name=data['chat_name'])

    # send request to user server to generate encryption key
    pass # TODO make it)

    # send response
    return jsonify({
        'chat_id': chat.id,
        'image_href': chat.image_href
        }), 201
