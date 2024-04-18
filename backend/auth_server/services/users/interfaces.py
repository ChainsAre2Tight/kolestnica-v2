"""Provides interfaces for user actors"""


from abc import ABC, abstractmethod

from libraries.utils.my_dataclasses import CurrentUser


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
        ) -> CurrentUser:
        """Attempts to create a user with provided username, login and password hash and returns \
            his data if successful
        
        :params str username: unique username
        :params str login: unique login credential (email)
        :params str pwdh: MD5 hash of user's password

        :returns: dataclass containing all relevant data of the user

        :raises:
            DuplicateLoginException: if there already is an account associated with \
                this login (email)
            DuplicateUsernameException: if there already is an account with specified username
        """
