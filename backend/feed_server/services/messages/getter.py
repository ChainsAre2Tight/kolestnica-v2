"""Provides an object that can read and list messages"""


from libraries.database.models import Message

from feed_server.services.messages.interfaces import MessageGetterInterface
import feed_server.helpers.quiries_helpers as quiry
from feed_server.helpers.access_helpers import verify_user_in_chat, verify_message_belongs_to_chat


class MessageGetter(MessageGetterInterface):

    @staticmethod
    def get_message(chat_id: int, message_id: int, browser_fingerprint: str) -> Message:

        user_id = quiry.get_user_id_by_browser_fingerprint(browser_fingerprint=browser_fingerprint)

        chat = quiry.get_chat_by_id(chat_id=chat_id)
        verify_user_in_chat(chat=chat, user_id=user_id)

        verify_message_belongs_to_chat(chat=chat, message_id=message_id)
        message = quiry.get_message_by_id(message_id=message_id)

        return message

    @staticmethod
    def list_messages(chat_id: int, browser_fingerprint: str) -> list[Message]:

        user_id = quiry.get_user_id_by_browser_fingerprint(browser_fingerprint=browser_fingerprint)
        chat = quiry.get_chat_by_id(chat_id=chat_id)
        verify_user_in_chat(chat=chat, user_id=user_id)

        messages = quires.get_messages_by_chat_id(chat_id=chat.id)
        return messages
