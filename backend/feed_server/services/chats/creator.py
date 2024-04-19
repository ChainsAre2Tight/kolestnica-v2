"""Provides chat creator class"""


from libraries.database import models

from feed_server import db, celery
from feed_server.services.chats.interfaces import ChatCreatorInterface
import feed_server.helpers.quiries_helpers as quiry


class ChatCreator(ChatCreatorInterface):

    @classmethod
    def create(cls, chat_name: str, browser_fingerprint: str) -> models.Chat:

        # get data
        user_id = quiry.get_user_id_by_browser_fingerprint(browser_fingerprint=browser_fingerprint)
        user = quiry.get_user_by_id(user_id=user_id)

        # create model
        chat = cls._construct(chat_name=chat_name, user=user)
        db.session.add(chat)
        db.session.commit()

        # send task to notification server
        ChatCreator._notify(user=user, chat_id=chat.id)

        return chat

    @staticmethod
    def _generate_key() -> str:
        # some keygen shenanigans
        return 'secretchatencryptionkey'

    @staticmethod
    def _construct(chat_name, user: models.User) -> models.Chat:
        chat = models.Chat(
            name=chat_name,
            messages=[],
            users=[user],
            encryption_key=ChatCreator._generate_key()
        )
        return chat

    @staticmethod
    def _notify(user: models.User, chat_id: int) -> None:
        for session in user.sessions:
            if session.socketId is not None:
                celery.send_task('tasks.create_chat', (session.socketId, chat_id))
