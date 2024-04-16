"""Provides interfaces for token actors"""


from abc import ABC, abstractmethod

from libraries.utils.my_dataclasses import SignedTokenPair, Token

class SignatoryIntarface(ABC):

    @staticmethod
    @abstractmethod
    def sign_token(token: Token) -> str:
        pass


class TokenPairCreatorIntarface(ABC):

    @staticmethod
    @abstractmethod
    def create(browser_fingerprint: str) -> SignedTokenPair:
        pass
