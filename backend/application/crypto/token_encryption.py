"""This module provides a controller that oversees token encryption"""

import os
from functools import wraps

import crypto.interfaces as interface
import crypto.strategies as strategy
from utils.wrapper_checks import check_for_keyword_in_kwargs


class TokenEncryptionController(interface.TokenEncryptionControllerInterface):

    def __init__(self, encryption: interface.EncryptionStrategyInterface):
        self._strategy = encryption()
        self._key = os.environ.get('TOKEN_ENCRYPTION_KEY') or None

    def encrypt_token(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            token: str = func(*args, **kwargs)

            return self._strategy.encrypt_message(message=token, encryption_key=self._key)
        return decorated_function

    def decrypt_token(self, keyword: str='token'):
        def wrapper(func):
            @wraps(func)
            def decorated_function(*args, **kwargs):
                check_for_keyword_in_kwargs(kwargs, keyword, func.__name__)
                encrypted_token: str = kwargs[keyword]

                decrypted_token: str = self._strategy.decrypt_message(
                    encrypted_token,
                    decryption_key=self._key
                )
                kwargs[keyword] = decrypted_token

                return func(*args, **kwargs)
            return decorated_function
        return wrapper

    @staticmethod
    def build():
        match os.environ.get('TOKEN_ENCRYPTION_STRATEGY'):
            case 'REVERSE':
                encryption = strategy.ReverseEncryptionStrategy
            case 'CAESAR':
                encryption = strategy.CaesarEncryptionStrategy
            case _:
                encryption = strategy.IdleEncryptionStrategy
        return TokenEncryptionController(encryption)
