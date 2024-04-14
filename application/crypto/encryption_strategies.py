from abc import ABC, abstractmethod


class EncryptionStrategyInterface(ABC):

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

class IdleEncryptionStrategy(EncryptionStrategyInterface):
    
    @staticmethod
    def encrypt_message(message: str, encryption_key: int | None = None) -> str:
        return message
    
    @staticmethod
    def decrypt_message(encrypted_message: str, decryption_key: int | None = None) -> str:
        return encrypted_message

class ReverseEncryptionStrategy(EncryptionStrategyInterface):

    @staticmethod
    def encrypt_message(message: str, **options) -> str:
        return message[::-1]
    
    @staticmethod
    def decrypt_message(message: str, **options) -> str:
        return message[::-1]

class CaesarEncryptionStrategy(EncryptionStrategyInterface):

    @staticmethod
    def encrypt_message(message: str, encryption_key: int | None = None) -> str:
        
        return ''.join([
            chr(ord(char) + encryption_key)
            for char in message
        ])
    
    @staticmethod
    def decrypt_message(encrypted_message: str, decryption_key: int | None = None) -> str:
        return ''.join([
            chr(ord(char) - decryption_key)
            for char in encrypted_message
        ])
