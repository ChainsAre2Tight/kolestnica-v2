import database.models as models
from feed.app import app, db
import utils.my_dataclasses as dataclass

def _get_user_by_sessionId(sessionId: str) -> models.Session:
    return db.session.query(models.Session).\
        filter(models.Session.uuid == sessionId).one().user


def _get_chats_by_session(user: models.User) -> list[models.Chat]:
    result = db.session.query(models.Chat)\
        .filter(models.Chat.users.any(models.User.id == user.id)).all()
    return result

def _get_users_by_chats(chats: list[models.Chat]) -> list[models.User]:
    users = db.session.query(models.User)\
        .filter(models.User.chats.any(
            models.Chat.id.in_([chat.id for chat in chats])
        ))
    return users

def _get_messages_by_chat_id_and_user(chat_id: int, user: models.User) -> list[models.Message]:
    # TODO if user is not in chat raise an exception
    messages = db.session.query(models.Message).filter(
        models.Message.chat_id == chat_id,
        models.Message.chat.has(models.Chat.users.any(models.User.id == user.id))
    ).all()
    return messages

def get_chats_by_sessionId(sessionId: str) -> list[dataclass.Chat]:
    return dataclass.convert_model_to_dataclass(
        _get_chats_by_session(
            _get_user_by_sessionId(
                sessionId=sessionId
            )),
        dataclass.Chat
    )

def get_users_by_sessionId(sessionId: str) -> list[dataclass.OtherUser]:
    return dataclass.convert_model_to_dataclass(
        _get_users_by_chats(
            _get_chats_by_session(
                _get_user_by_sessionId(sessionId=sessionId)
            )
        ),
        dataclass.OtherUser
    )

def get_messages_by_chat_id(chat_id: int, sessionId: str) -> list[dataclass.Message]:
    return dataclass.convert_model_to_dataclass(
        _get_messages_by_chat_id_and_user(
            chat_id=chat_id,
            user=_get_user_by_sessionId(sessionId=sessionId)
        ),
        dataclass.Message
    )