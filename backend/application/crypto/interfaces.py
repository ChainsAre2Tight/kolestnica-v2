"""Provides interfaces for cryptography objetcs"""
from abc import ABC, abstractmethod
from typing_extensions import Callable


class EncryptionStrategyInterface(ABC):
    """Interface for encryption strategies"""
    key_format: type

    @staticmethod
    @abstractmethod
    def encrypt_message(
            message: str,
            encryption_key: int | None = None
        ) -> str:
        """Encrypts a string using provided encryption key

        Args:
            message (str): message that needs to be encrypted
            encryption_key (int | None, optional): Key used for encryption. Defaults to None.

        Returns:
            str: Encrypted message
        """

    @staticmethod
    @abstractmethod
    def decrypt_message(
            encrypted_message: str,
            decryption_key: int | None = None
        ) -> str:
        """Decrypts a string with provided decryption key

        Args:
            encrypted_message (str): message that needs to be decrypted
            decryption_key (int | None, optional): Key used for decryption. Defaults to None.

        Returns:
            str: Decrypted message
        """

    @classmethod
    @abstractmethod
    def format_key(cls, key: str) -> object:
        """Formats key into format needed for this encryption algorithm

        Args:
            key (str): key from request headers

        Raises:
            BadEncryptionKeys: If key is missing or is in wrong format

        Returns:
            object: key of required type
        """


class JSONEncryptionControllerInterface(ABC):
    _encryption_strategy: EncryptionStrategyInterface

    @abstractmethod
    def encrypt_json(self, provide_data: bool = False) -> Callable:
        """A decorator that will encrypt and decrypt json of decorated requests

        Args:
            provide_data (bool, optional): If set to True will provide "data" attribute\
        to decorated functions containing decrypted JSON data. Defaults to False.

        Raises:
            BadEncryptionKeys: If header containing keys is missing or keys are in wrong format
            NotImplementedError: If JSON contains data that cannot be encrypted
        """

    @staticmethod
    @abstractmethod
    def build():
        """Build a JSON encryption controller based on current environment

        Returns:
            JSONEncryptionController: controller instance
        """

class TokenEncryptionControllerInterface(ABC):
    _strategy: EncryptionStrategyInterface
    _key: str

    @abstractmethod
    def encrypt_token(self, func):
        """Encrypts the token string with a symmetric cryptoalgorithm"""

    @abstractmethod
    def decrypt_token(self, keyword: str = 'token'):
        """Decrypts the token string with a symmetric cryptoalgorithm
        
        :params str keyword: Key of KWARGS by which to look for token
        """

    @staticmethod
    @abstractmethod
    def build():
        """Build a token encryption controller based on current environment

        Returns:
            _type_: A token encryption controller instance
        """
