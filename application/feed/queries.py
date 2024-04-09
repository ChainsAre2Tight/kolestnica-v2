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
