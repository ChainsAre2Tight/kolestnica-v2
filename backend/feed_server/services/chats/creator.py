"""Provides chat creator class"""


from libraries.utils.my_dataclasses import Chat
from libraries.database import models

from feed_server import db
from feed_server.services.chats.interfaces import ChatCreatorInterface
from feed_server.helpers.quiries_helpers import get_user_by_id


class ChatCreator(ChatCreatorInterface):

    @classmethod
    def create(cls, chat_name: str, user_id: int) -> Chat:
        user = get_user_by_id(user_id=user_id)
        chat = cls._construct(chat_name=chat_name, user=user)
        db.session.add(chat)
        db.session.commit()

        chat_data = Chat.from_model(chat)
        return chat_data

    @staticmethod
    def _construct(chat_name, user: models.User) -> models.Chat:
        chat = models.Chat(
            name=chat_name,
            messages=[],
            users=[user]
        )
        return chat
