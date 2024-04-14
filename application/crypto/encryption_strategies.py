from abc import ABC, abstractmethod


class EncryptionStrategyInterface(ABC):

    @abstractmethod
    def encrypt_message(self, message: str) -> str:
        pass

    @abstractmethod
    def decrypt_message(self, message: str) -> str:
        pass

class IdleEncryptionStrategy(EncryptionStrategyInterface):
    
    def encrypt_message(self, message: str) -> str:
        return message
    
    def decrypt_message(self, message: str) -> str:
        return message

class ReverseEncryptionStrategy(EncryptionStrategyInterface):

    def encrypt_message(self, message: str) -> str:
        return message[::-1]
    
    def decrypt_message(self, message: str) -> str:
        return message[::-1]
