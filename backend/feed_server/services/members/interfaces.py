"""Provides interfaces for managing members of chats"""


from abc import ABC, abstractmethod

from libraries.utils.my_dataclasses import OtherUser


class MemberListerInterface(ABC):

    @staticmethod
    @abstractmethod
    def list_members(chat_id: int, issuer_id: int) -> list[OtherUser]:
        pass


class MemberAdderInterface(ABC):

    @staticmethod
    @abstractmethod
    def add_member(chat_id: int, issuer_id: int, target_id: int) -> list[OtherUser]:
        pass


class MemberRemoverInterface(ABC):

    @staticmethod
    @abstractmethod
    def remove_member(chat_id: int, issuer_id: int, target_id: int) -> list[OtherUser]:
        pass
