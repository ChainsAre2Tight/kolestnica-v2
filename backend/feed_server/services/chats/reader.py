"""Contains chat reader class"""


from libraries.utils.my_dataclasses import Chat

from feed_server.services.chats.interfaces import ChatReaderInterface
from feed_server.helpers.quiries_helpers import get_chat_by_id
from feed_server.helpers.access_helpers import verify_user_in_chat


class ChatReader(ChatReaderInterface):

    @classmethod
    def get_chat_data(cls, chat_id: int, user_id: int) -> Chat:
        chat = get_chat_by_id(chat_id=chat_id)
        verify_user_in_chat(chat, user_id)
        return Chat.from_model(chat)
