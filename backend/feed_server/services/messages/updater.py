"""Provides object that can update messages"""


from feed_server import db
from feed_server.services.messages.interfaces import MessageUpdaterInterface
from feed_server.helpers.quiries_helpers import get_chat_by_id, get_message_by_id
import feed_server.helpers.access_helpers as access


class MessageUpdater(MessageUpdaterInterface):

    @staticmethod
    def update_body(user_id: int, chat_id: int, message_id: int, new_body: str) -> int:

        chat = get_chat_by_id(chat_id=chat_id)
        access.verify_user_in_chat(chat=chat, user_id=user_id)

        access.verify_message_belongs_to_chat(chat=chat, message_id=message_id)
        message = get_message_by_id(message_id=message_id)

        access.verify_message_authorship(message=message, user_id=user_id)
        message.body = new_body
        db.session.commit()

        return message.id
