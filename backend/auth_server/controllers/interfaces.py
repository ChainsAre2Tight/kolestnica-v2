"""This module provides interfaces for auth server HTTP controllers"""


from abc import ABC, abstractmethod
from flask import Response

from libraries.utils.my_dataclasses import Token


class UserControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def register_user(data: dict) -> tuple[Response, int]:
        """Registers user"""


class SessionControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def login_user(data: dict) -> tuple[Response, int]:
        """Logs user in"""

    @staticmethod
    @abstractmethod
    def logout(access_token: Token) -> tuple[Response, int]:
        """Logs user out"""

    @staticmethod
    @abstractmethod
    def list_sessions(access_token: Token) -> tuple[Response, int]:
        """Lists all currently active sessions of this user"""


class TokenControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def refresh_tokens(
            raw_token: str,
            refresh_token: Token
        ) -> tuple[Response, int]:
        """Provides user with a fresh pair of tokens"""
