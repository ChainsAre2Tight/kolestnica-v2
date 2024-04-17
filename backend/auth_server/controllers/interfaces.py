"""This module provides interfaces for auth server HTTP controllers"""


from abc import ABC, abstractmethod
from flask import Response

from libraries.utils.my_dataclasses import Token


class UserControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def show(access_token: Token, user_id: int) -> tuple[Response, int]:
        """Gets info of a certain user"""

    @staticmethod
    @abstractmethod
    def show_current(access_token: Token) -> tuple[Response, int]:
        """Gets current user's data"""

    @staticmethod
    @abstractmethod
    def create(data: dict) -> tuple[Response, int]:
        """Registers user"""


class SessionControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def index(access_token: Token) -> tuple[Response, int]:
        """Lists all currently active sessions of this user"""

    @staticmethod
    @abstractmethod
    def create(data: dict) -> tuple[Response, int]:
        """Logs user in"""

    @staticmethod
    @abstractmethod
    def delete_current(access_token: Token) -> tuple[Response, int]:
        """Logs user out"""


class TokenControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def refresh(
            raw_token: str,
            refresh_token: Token
        ) -> tuple[Response, int]:
        """Provides user with a fresh pair of tokens"""
