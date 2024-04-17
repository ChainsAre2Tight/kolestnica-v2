"""Contains chat reader class"""


from libraries.utils.my_dataclasses import Chat, convert_model_to_dataclass

from feed_server.services.chats.interfaces import ChatReaderInterface
from feed_server.helpers.quiries_helpers import get_chat_by_id, get_user_by_id
from feed_server.helpers.access_helpers import verify_user_in_chat


class ChatReader(ChatReaderInterface):

    @staticmethod
    def get_chat_data(chat_id: int, user_id: int) -> Chat:
        chat = get_chat_by_id(chat_id=chat_id)
        verify_user_in_chat(chat, user_id)
        return Chat.from_model(chat)

    @staticmethod
    def get_chats(user_id: int) -> list[Chat]:
        user = get_user_by_id(user_id=user_id)
        chats = convert_model_to_dataclass(
            objects=user.chats,
            target_dataclass=Chat
        )
        return chats
