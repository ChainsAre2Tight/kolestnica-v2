"""Provides interface for feed server controllers"""


from abc import ABC, abstractmethod

from flask import Response

from libraries.utils.my_dataclasses import Token


class ChatControllerIntarface(ABC):

    @staticmethod
    @abstractmethod
    def get_chats(access_token: Token) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def create_chat(access_token: Token, data: dict) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def get_chat_data(access_token: Token, chat_id: int) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def delete_chat(access_token: Token, chat_id: int) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def update_chat(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:
        pass


class MessageControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def list_messages(access_token: Token, chat_id: int) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def get_message(access_token: Token, chat_id: int, message_id: int) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def create_message(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def delete_message(access_token: Token, chat_id: int, message_id: int) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def update_message(
            access_token: Token,
            chat_id: int,
            message_id: int,
            data: dict
        ) -> tuple[Response, int]:
        pass


class MembersControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def get_members(access_token: Token, chat_id: int) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def add_member(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def remove_member(access_token: Token, chat_id: int, target_id: int) -> tuple[Response, int]:
        pass
