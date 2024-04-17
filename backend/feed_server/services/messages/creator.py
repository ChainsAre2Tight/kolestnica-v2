"""Provides object that can create messages"""


from libraries.database.models import Message

from feed_server import db
from feed_server.services.messages.interfaces import MessageCreatorInterface
from feed_server.helpers.quiries_helpers import get_chat_by_id, get_user_id_by_browser_fingerprint
from feed_server.helpers.access_helpers import verify_user_in_chat


class MessageCreator(MessageCreatorInterface):

    @staticmethod
    def create_message(
            chat_id: int,
            text: str,
            timestamp: int,
            browser_fingerprint: str
        ) -> int:

        user_id = get_user_id_by_browser_fingerprint(browser_fingerprint=browser_fingerprint)
        chat = get_chat_by_id(chat_id=chat_id)
        verify_user_in_chat(chat=chat, user_id=user_id)

        message = Message(
            body=text,
            timestamp=timestamp,
            author_id=user_id,
            chat_id=chat_id
        )

        db.session.add(message)
        db.session.commit()

        return message.id
