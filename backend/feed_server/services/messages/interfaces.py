"""Provides interfaces for message manipulations"""


from abc import ABC, abstractmethod

from libraries.database.models import Message


class MessageGetterInterface(ABC):

    @staticmethod
    @abstractmethod
    def list_messages(chat_id: int, browser_fingerprint: str) -> list[Message]:
        pass

    @staticmethod
    @abstractmethod
    def get_message(chat_id: int, message_id: int, browser_fingerprint: str) -> Message:
        pass


class MessageCreatorInterface(ABC):

    @staticmethod
    @abstractmethod
    def create_message(
            chat_id: int,
            text: str,
            timestamp: int,
            browser_fingerprint: str
        ) -> Message:
        pass


class MessageUpdaterInterface(ABC):

    @staticmethod
    @abstractmethod
    def update_body(
            chat_id: int,
            message_id: int,
            new_body: str,
            browser_fingerprint: str
        ) -> Message:
        pass


class MessageDeleterInterface(ABC):

    @staticmethod
    @abstractmethod
    def delete_message(chat_id: int, message_id: int, browser_fingerprint: str) -> Message:
        pass


class MessageSerializerInterface(ABC):

    @staticmethod
    @abstractmethod
    def to_id(message: Message) -> int:
        pass

    @staticmethod
    @abstractmethod
    def full(message: Message) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def full_list(messages: list[Message]) -> list[dict]:
        pass
