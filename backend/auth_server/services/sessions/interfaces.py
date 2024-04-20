"""Provides interfaces for session actors"""


from abc import ABC, abstractmethod

from libraries.database.models import Session


class SessionReaderIntarface(ABC):

    @staticmethod
    @abstractmethod
    def read(browser_fingerprint: str) -> Session:
        """Finds a session with this fingerprint"""


class SessionCreatorInterface(ABC):

    @staticmethod
    @abstractmethod
    def create(
            login: str,
            pwdh: str,
            browser_fingerprint: str
        ) -> Session:
        """Logs user in by creating a session for them

        Args:
            login (str): login
            pwdh (str): MD5 of user's password
            browser_fingerprint (str): unique browser fingerprint

        Returns:
            Session: dataclass with session data
        
        Raises:
            AlreadyLoggedIn: if user has already logged in to a different acc from the same device
            InvalidLoginData: if provided login/password do not match any records
        """


class SessionUpdaterIntarface(ABC):

    @staticmethod
    @abstractmethod
    def update_refresh_token(
            browser_fingerprint: str,
            new_refresh_token: str
        ) -> None:
        """Updates Session model with a new refresh token"""

    @staticmethod
    @abstractmethod
    def update_socket_id(
            browser_fingerprint: str,
            new_socket_id: str
        ) -> None:
        """Updates Session models with a new SocketIO socket id"""


class SessionDeleterInterface(ABC):

    @staticmethod
    @abstractmethod
    def delete(browser_fingerprint: str) -> None:
        """Attempts to terminate a session associated with this broser fingerprint

        :params str browser_fingerprint: fingerprint of current session, accesible via provided JWT

        :raises SessionNotFound: if session with provided data cannot be found
        """


class SessionSerializerInterface(ABC):

    @staticmethod
    @abstractmethod
    def full(session: Session) -> dict:
        """А этот метод возвращает березовый конденсатор, потому что читать это никто не будет"""

    @staticmethod
    @abstractmethod
    def full_list(sessions: list[Session]) -> list[dict]:
        pass
