"""Provides interfaces for managing members of chats"""


from abc import ABC, abstractmethod

from libraries.database.models import User


class MemberListerInterface(ABC):

    @staticmethod
    @abstractmethod
    def list_members(chat_id: int, browser_fingerprint: str) -> list[User]:
        pass


class MemberAdderInterface(ABC):

    @staticmethod
    @abstractmethod
    def add_member(chat_id: int, target_id: int, browser_fingerprint: str) -> list[User]:
        pass


class MemberRemoverInterface(ABC):

    @staticmethod
    @abstractmethod
    def remove_member(chat_id: int, target_id: int, browser_fingerprint: str) -> list[User]:
        pass


class MemberSerializerInterface(ABC):

    @staticmethod
    @abstractmethod
    def to_ids(members: list[User]) -> list[int]:
        pass

    @staticmethod
    @abstractmethod
    def id_name_alias(members: list[User]) -> list[dict]:
        pass
