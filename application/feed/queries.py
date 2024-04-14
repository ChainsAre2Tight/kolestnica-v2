import database.models as models
from feed.app import app, db
import utils.my_dataclasses as dataclass
import sqlalchemy.exc
import utils.my_exceptions as exc
from database.cache_controller import CacheController


@CacheController.read_through_cache('sessionId')
def get_user_id_by_sessionId(sessionId: str) -> int:
    try:
        return db.session.query(models.Session).\
            filter(models.Session.uuid == sessionId).one().user_id
    except sqlalchemy.exc.NoResultFound:
        raise exc.UserNotExistsException

def get_user_by_id(user_id: int) -> models.User:
    user = db.session.get(models.User, user_id)
    if user is None:
        raise exc.UserNotExistsException
    return user

def _get_chats_by_session(user_id: int) -> list[models.Chat]:
    result = db.session.query(models.Chat)\
        .filter(models.Chat.users.any(models.User.id == user_id)).all()
    return result

def _get_users_by_chats(chats: list[models.Chat]) -> list[models.User]:
    users = db.session.query(models.User)\
        .filter(models.User.chats.any(
            models.Chat.id.in_([chat.id for chat in chats])
        ))
    return users

def _get_messages_by_chat_id_and_user(chat_id: int, user_id: int) -> list[models.Message]:
    try:
        chat = db.session.query(models.Chat)\
            .filter(
                models.Chat.id == chat_id,
                models.Chat.users.any(models.User.id == user_id)
            ).one()
    except sqlalchemy.exc.NoResultFound:
        raise exc.NoAcccessException(f'User #{user_id} Attempted to access chat №{chat_id}')

    messages = db.session.query(models.Message).filter(
        models.Message.chat_id == chat.id
    ).all()
    return messages

def get_chats_by_sessionId(sessionId: str) -> list[dataclass.Chat]:
    return dataclass.convert_model_to_dataclass(
        _get_chats_by_session(
            get_user_id_by_sessionId(sessionId=sessionId)),
        dataclass.Chat
    )

def get_users_by_sessionId(sessionId: str) -> list[dataclass.OtherUser]:
    return dataclass.convert_model_to_dataclass(
        _get_users_by_chats(
            _get_chats_by_session(
                get_user_id_by_sessionId(sessionId=sessionId)
            )
        ),
        dataclass.OtherUser
    )

def get_messages_by_chat_id(chat_id: int, sessionId: str) -> list[dataclass.Message]:
    return dataclass.convert_model_to_dataclass(
        _get_messages_by_chat_id_and_user(
            chat_id=chat_id,
            user_id=get_user_id_by_sessionId(sessionId=sessionId)
        ),
        dataclass.Message
    )

def store_message(sessionId: str, message: dataclass.Message) -> dataclass.Message:
    
    # get user info from database
    user_id = get_user_id_by_sessionId(sessionId=sessionId)

    message.author_id = user_id

    # send messsage to database
    model_message: models.Message = message.to_model(model=models.Message)
    db.session.add(model_message)
    db.session.commit()
    
    # update dataclass info
    message.id = model_message.id

    return message

def delete_message(sessionId: str, chat_id: int, message_id: int) -> dict[str, int]:

    # get user info from database
    user_id = get_user_id_by_sessionId(sessionId=sessionId)

    user = get_user_by_id(user_id)
    if chat_id not in [chat.id for chat in user.chats]:
        raise exc.NoAcccessException

    # get message info from database
    try:
        message = db.session.query(models.Message).filter(
            models.Message.id == message_id,
            models.Message.chat_id == chat_id
        ).one()
    except sqlalchemy.exc.NoResultFound:
        raise exc.NoAcccessException

    # verify his authorship
    if message.author_id != user_id:
        raise exc.NotPermittedException

    # delete message
    msg_to_delete = {'chat_id': message.chat_id, 'msg_id': message.id}
    db.session.delete(message)
    db.session.commit()

    return msg_to_delete

def create_chat(sessionId: str, chat_name: str) -> dataclass.Chat:
    
    # get user data
    user_id = get_user_id_by_sessionId(sessionId=sessionId)

    user = get_user_by_id(user_id)

    # create chat
    chat = models.Chat(
        name=chat_name,
        users=[user]
    )
    db.session.add(chat)
    db.session.commit()

    # return its data
    return dataclass.Chat.from_model(chat)
    
def get_users_of_certain_chat(sessionId: str, chat_id: int) -> list[dataclass.OtherUser]:
    
    user_id = get_user_id_by_sessionId(sessionId=sessionId)

    user = get_user_by_id(user_id)
    if chat_id not in [chat.id for chat in user.chats]:
        raise exc.NoAcccessException
    
    users = db.session.get(models.Chat, chat_id).users

    return dataclass.convert_model_to_dataclass(users, dataclass.OtherUser)

def add_user_to_chat(sessionId: str, chat_id: int, username: str) -> dataclass.OtherUser:

    user_id = get_user_id_by_sessionId(sessionId=sessionId)

    user = get_user_by_id(user_id)
    if chat_id not in [chat.id for chat in user.chats]:
        raise exc.NoAcccessException
    
    # TODO add administative rights check
    try:
        user_to_add = db.session.query(models.User).filter(
            models.User.username == username
        ).one()
    except sqlalchemy.exc.NoResultFound:
        raise exc.UserNotFoundException
    
    # if user is already in chat
    if chat_id in [chat.id for chat in user_to_add.chats]:
        raise exc.RequestAlreadyFullfilledException

    chat = db.session.get(models.Chat, chat_id)
    chat.users.append(user_to_add)
    db.session.commit()

    return dataclass.OtherUser.from_model(user_to_add)
