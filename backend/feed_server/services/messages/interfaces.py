"""Provides interfaces for message manipulations"""


from abc import ABC, abstractmethod

from libraries.utils.my_dataclasses import Message


class MessageGetterInterface(ABC):

    @staticmethod
    @abstractmethod
    def list_messages(user_id: int, chat_id: int) -> list[Message]:
        pass

    @staticmethod
    @abstractmethod
    def get_message(user_id: int, chat_id: int, message_id: int) -> Message:
        pass


class MessageCreatorInterface(ABC):

    @staticmethod
    @abstractmethod
    def create_message(user_id: int, chat_id: int, text: str, timestamp: int) -> int:
        pass


class MessageDeleterInterface(ABC):

    @staticmethod
    @abstractmethod
    def delete_message(user_id: int, chat_id: int, message_id: int) -> int:
        pass
