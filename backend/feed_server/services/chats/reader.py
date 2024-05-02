"""Contains chat reader class"""

from libraries.database.models import Chat

from feed_server.services.chats.interfaces import ChatReaderInterface
import feed_server.helpers.quiries_helpers as quiry
from feed_server.helpers.access_helpers import verify_user_in_chat


class ChatReader(ChatReaderInterface):

    @staticmethod
    def get_chat_data(chat_id: int, browser_fingerprint: str) -> Chat:
        user_id = quiry.get_user_id_by_browser_fingerprint(browser_fingerprint=browser_fingerprint)
        chat = quiry.get_chat_by_id(chat_id=chat_id)
        verify_user_in_chat(chat, user_id)
        return chat

    @staticmethod
    def get_chats(browser_fingerprint: str) -> list[Chat]:
        user_id = quiry.get_user_id_by_browser_fingerprint(browser_fingerprint=browser_fingerprint)
        user = quiry.get_user_by_id(user_id=user_id)
        chats = quiry.get_chats_by_user(user=user)
        return chats
