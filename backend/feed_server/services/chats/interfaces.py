"""Provides services for chat management"""


from abc import ABC, abstractmethod

from libraries.utils.my_dataclasses import Chat


class ChatCreatorInterface(ABC):

    @classmethod
    @abstractmethod
    def create(cls, chat_name: str, user_id: int) -> Chat:
        pass


class ChatReaderInterface(ABC):

    @classmethod
    @abstractmethod
    def get_chat_data(cls, chat_id: int, user_id: int) -> Chat:
        pass
