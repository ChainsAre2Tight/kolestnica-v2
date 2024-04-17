"""Provides services for chat management"""


from abc import ABC, abstractmethod

from libraries.utils.my_dataclasses import Chat


class ChatCreatorInterface(ABC):

    @classmethod
    @abstractmethod
    def create(cls, chat_name: str, user_id: int) -> Chat:
        pass


class ChatReaderInterface(ABC):

    @staticmethod
    @abstractmethod
    def get_chats(browser_fingerprint: str) -> list[Chat]:
        pass

    @staticmethod
    @abstractmethod
    def get_chat_data(chat_id: int, browser_fingerprint: str) -> Chat:
        pass
