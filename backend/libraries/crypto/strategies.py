"""Module containing encryption stretegies

Alivable strategies:
- Idle
- Reverse
- Caesar cipher
- RSA (TBA)
"""

from utils.exc import BadEncryptionKeys
from crypto.interfaces import EncryptionStrategyInterface


class IdleEncryptionStrategy(EncryptionStrategyInterface):
    """Performs no encryption"""
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
    """Reverses given messages"""
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
    """Is essaentialy a Caesar cipher
    
    - Shifts ord() of given charactes by amount specified in key
    - Shifts integers by key
    
    Key format: Integer
    """
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
