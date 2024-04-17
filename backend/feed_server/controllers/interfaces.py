"""Provides interface for feed server controllers"""


from abc import ABC, abstractmethod

from flask import Response

from libraries.utils.my_dataclasses import Token


class ChatControllerIntarface(ABC):

    @staticmethod
    @abstractmethod
    def index(access_token: Token) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def show(access_token: Token, chat_id: int) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def create(access_token: Token, data: dict) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def update(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def delete(access_token: Token, chat_id: int) -> tuple[Response, int]:
        pass


class MessageControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def index(access_token: Token, chat_id: int) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def show(access_token: Token, chat_id: int, message_id: int) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def create(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def update(
            access_token: Token,
            chat_id: int,
            message_id: int,
            data: dict
        ) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def delete(access_token: Token, chat_id: int, message_id: int) -> tuple[Response, int]:
        pass


class MembersControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def index(access_token: Token, chat_id: int) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def create(access_token: Token, chat_id: int, data: dict) -> tuple[Response, int]:
        pass

    @staticmethod
    @abstractmethod
    def delete(access_token: Token, chat_id: int, target_id: int) -> tuple[Response, int]:
        pass
