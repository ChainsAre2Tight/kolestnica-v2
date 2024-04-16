"""Provides various quiries used throughout feed service"""


from sqlalchemy.exc import NoResultFound

from libraries.utils.exc import UserNotExistsException, UserNotFoundException, ChatNotFound, MessageNotFound
from libraries.cache import cache_controller
from libraries.database.models import Session, User, Chat, Message

from feed_server import db

@cache_controller.read_through_cache('browser_fingerprint', int)
def get_user_id_by_browser_fingerprint(browser_fingerprint: str) -> int:
    try:
        user_id = db.session.query(Session).filter(
                Session.uuid == browser_fingerprint
            ).one().user_id
    except NoResultFound:
        raise UserNotExistsException(f'session {browser_fingerprint} does not exist')
    return user_id

def get_user_by_id(user_id: int) -> User:
    try:
        user = db.session.query(User).filter(User.id == user_id).one()
    except NoResultFound:
        raise UserNotFoundException(f'User with id {user_id} cannot be found')
    return user

def get_chat_by_id(chat_id: int) -> Chat:
    try:
        chat = db.session.query(Chat).filter(Chat.id == chat_id).one()
    except NoResultFound:
        raise ChatNotFound(f'Chat with id {chat_id} does not exist')
    return chat

def get_message_by_id(message_id: int) -> Message:
    try:
        message = db.session.query(Message).filter(Message.id == message_id).one()
    except NoResultFound:
        raise MessageNotFound(f'Message with id {message_id} does not exist')
    return message
