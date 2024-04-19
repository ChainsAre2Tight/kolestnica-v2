"""Provides interfaces for user actors"""


from abc import ABC, abstractmethod

from libraries.database.models import User


class UserReaderInterface(ABC):

    @staticmethod
    @abstractmethod
    def index_chats(browser_fingerprint: str) -> list[int]:
        pass


class UserCreatorIntarface(ABC):

    @staticmethod
    @abstractmethod
    def create(
            username: str,
            login: str,
            pwdh: str
        ) -> User:
        """Attempts to create a user with provided username, login and password hash and returns \
            his data if successful
        
        :params str username: unique username
        :params str login: unique login credential (email)
        :params str pwdh: MD5 hash of user's password

        :returns: User

        :raises:
            DuplicateLoginException: if there already is an account associated with \
                this login (email)
            DuplicateUsernameException: if there already is an account with specified username
        """


class UserSerializatorInterface(ABC):

    @staticmethod
    @abstractmethod
    def to_id(user: User) -> int:
        pass

    @staticmethod
    @abstractmethod
    def full(user: User) -> dict:
        pass
