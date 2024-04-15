"""This module provides a controller that oversees token encryption"""

import os
from functools import wraps

from crypto.encryption_strategies import *
from utils.wrapper_checks import check_for_keyword_in_kwargs


class TokenEncryptionController():
    _strategy: EncryptionStrategyInterface
    _key: str
    
    def __init__(self, encryption: EncryptionStrategyInterface):
        self._strategy = encryption()
        self._key = os.environ.get('TOKEN_ENCRYPTION_KEY') or None

    def encrypt_token(self, func):
        """Encrypts the token string with a symmetric cryptoalgorithm"""
        @wraps(func)
        def decorated_function(*args, **kwargs):
            token: str = func(*args, **kwargs)

            return self._strategy.encrypt_message(message=token, encryption_key=self._key)
        return decorated_function
    
    def decrypt_token(self, keyword: str='token'):
        """Decrypts the token string with a symmetric cryptoalgorithm
        
        :params str keyword: Key of KWARGS by which to look for token
        """
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
    
    def build():
        """Build a token encryption controller based on current environment

        Returns:
            _type_: A token encryption controller instance
        """
        match os.environ.get('TOKEN_ENCRYPTION_STRATEGY'):
            case 'REVERSE':
                encryption = ReverseEncryptionStrategy
            case 'CAESAR':
                encryption = CaesarEncryptionStrategy
            case _:
                encryption = IdleEncryptionStrategy
        return TokenEncryptionController(encryption)
