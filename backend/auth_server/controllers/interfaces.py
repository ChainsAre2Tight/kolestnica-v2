"""This module provides interfaces for auth server HTTP controllers"""


from abc import ABC, abstractmethod
from flask import Response

from libraries.utils.my_dataclasses import Token


class KeyControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def show_public_key() -> tuple[Response, int]:
        """Sends user auth server public key"""


class UserControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def show_user(access_token: Token, user_id: int) -> tuple[Response, int]:
        """Gets info of a certain user"""

    @staticmethod
    @abstractmethod
    def show_current_user(access_token: Token) -> tuple[Response, int]:
        """Gets current user's data"""

    @staticmethod
    @abstractmethod
    def create_user(data: dict) -> tuple[Response, int]:
        """Registers user"""


class SessionControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def index_sessions(access_token: Token) -> tuple[Response, int]:
        """Lists all currently active sessions of this user"""

    @staticmethod
    @abstractmethod
    def create_session(data: dict) -> tuple[Response, int]:
        """Logs user in"""

    @staticmethod
    @abstractmethod
    def delete_current_session(access_token: Token) -> tuple[Response, int]:
        """Logs user out"""

    @staticmethod
    @abstractmethod
    def update_current_session(data: dict) -> tuple[Response, int]:
        """Updates user session with new socket id. For internal use only"""


class TokenControllerInterface(ABC):

    @staticmethod
    @abstractmethod
    def refresh(
            raw_token: str,
            refresh_token: Token
        ) -> tuple[Response, int]:
        """Provides user with a fresh pair of tokens"""
