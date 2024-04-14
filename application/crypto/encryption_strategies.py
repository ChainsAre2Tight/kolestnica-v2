from abc import ABC, abstractmethod
from utils.exc import BadEncryptionKeys


class EncryptionStrategyInterface(ABC):
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

class IdleEncryptionStrategy(EncryptionStrategyInterface):
    key_format = None
    
    @staticmethod
    def encrypt_message(message: str, encryption_key: int | None = None) -> str:
        return message
    
    @staticmethod
    def decrypt_message(encrypted_message: str, decryption_key: int | None = None) -> str:
        return encrypted_message
    
    @classmethod
    def format_key(cls, key: str) -> object:
        return None

class ReverseEncryptionStrategy(EncryptionStrategyInterface):
    key_format = None

    @staticmethod
    def encrypt_message(message: str, **options) -> str:
        return message[::-1]
    
    @staticmethod
    def decrypt_message(message: str, **options) -> str:
        return message[::-1]
    
    @classmethod
    def format_key(cls, key: str) -> object:
        return None

class CaesarEncryptionStrategy(EncryptionStrategyInterface):
    key_format = int

    @staticmethod
    def encrypt_message(message: str, encryption_key: int) -> str:
        if type(message) is int:
            return message + encryption_key
        return ''.join([
            chr(ord(char) + encryption_key)
            for char in message
        ])
    
    @staticmethod
    def decrypt_message(encrypted_message: str, decryption_key: int) -> str:
        if type(encrypted_message) is int:
            return encrypted_message - decryption_key
        return ''.join([
            chr(ord(char) - decryption_key)
            for char in encrypted_message
        ])
    
    @classmethod
    def format_key(cls, key: str) -> int:
        try:
            return cls.key_format(key)
        except ValueError:
            raise BadEncryptionKeys('Encryption key cannot be converted to integer')
