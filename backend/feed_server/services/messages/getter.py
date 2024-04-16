"""Provides an object that can read and list messages"""


from libraries.utils.my_dataclasses import Message, convert_model_to_dataclass

from feed_server.services.messages.interfaces import MessageGetterInterface
from feed_server.helpers.quiries_helpers import get_chat_by_id, get_message_by_id
from feed_server.helpers.access_helpers import verify_user_in_chat, verify_message_belongs_to_chat


class MessageGetter(MessageGetterInterface):

    @staticmethod
    def get_message(user_id: int, chat_id: int, message_id: int) -> Message:

        chat = get_chat_by_id(chat_id=chat_id)
        verify_user_in_chat(chat=chat, user_id=user_id)

        verify_message_belongs_to_chat(chat=chat, message_id=message_id)
        message = get_message_by_id(message_id=message_id)

        message_data = Message.from_model(message)
        return message_data

    @staticmethod
    def list_messages(user_id: int, chat_id: int) -> list[Message]:
        chat = get_chat_by_id(chat_id=chat_id)

        verify_user_in_chat(chat=chat, user_id=user_id)

        messages = convert_model_to_dataclass(
            chat.messages,
            Message
        )
        return messages
