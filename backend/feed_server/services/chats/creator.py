"""Provides chat creator class"""


import random

from libraries.database import models

from feed_server import db, celery
from feed_server.services.chats.interfaces import ChatCreatorInterface
import feed_server.helpers.quiries_helpers as quiry


SYMBOLS = '0123456789abcdef'


class ChatCreator(ChatCreatorInterface):

    @classmethod
    def create(cls, chat_name: str, chat_image_href: str, browser_fingerprint: str) -> models.Chat:

        # get data
        user_id = quiry.get_user_id_by_browser_fingerprint(browser_fingerprint=browser_fingerprint)
        user = quiry.get_user_by_id(user_id=user_id)

        # create model
        chat = cls._construct(chat_name=chat_name, user=user, image_href=chat_image_href)
        db.session.add(chat)
        db.session.commit()

        # send task to notification server
        ChatCreator._notify(user=user, chat_id=chat.id)

        return chat

    @staticmethod
    def _generate_key() -> str:
        key = ''.join(random.choices(SYMBOLS, k=16))
        return key

    @staticmethod
    def _construct(chat_name, image_href, user: models.User) -> models.Chat:
        if image_href != '':
            chat = models.Chat(
                name=chat_name,
                messages=[],
                users=[user],
                encryption_key=ChatCreator._generate_key(),
                image_href=image_href
            )
        else:
            chat = models.Chat(
                name=chat_name,
                messages=[],
                users=[user],
                encryption_key=ChatCreator._generate_key(),
            )
        return chat

    @staticmethod
    def _notify(user: models.User, chat_id: int) -> None:
        for session in user.sessions:
            if session.socketId is not None:
                celery.send_task('create_chat', (session.socketId, chat_id))
