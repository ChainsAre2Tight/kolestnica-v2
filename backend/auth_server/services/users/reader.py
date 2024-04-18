"""Provides user reader"""


from auth_server.services.users.interfaces import UserReaderInterface
from auth_server.helpers.queries_helpers import find_session_by_fingerprint


class UserReader(UserReaderInterface):

    @staticmethod
    def index_chats(browser_fingerprint: str) -> list[int]:
        session = find_session_by_fingerprint(browser_fingerprint=browser_fingerprint)
        user = session.user
        chats = user.chats
        return [chat.id for chat in chats]
