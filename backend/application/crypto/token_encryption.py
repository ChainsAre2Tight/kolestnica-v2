"""This module provides a controller that oversees token encryption"""

import os
from functools import wraps

from crypto.encryption_strategies import *
from utils.wrapper_checks import check_for_keyword_in_kwargs

# import relevant config
Environment = os.environ.get('ENVIRONMENT') or 'TEST'
if Environment == 'TEST':
    from project_config import TestGlobalConfig as GlobalConfig
elif Environment == 'PRODUCTION':
    from project_config import ProductionGlobalConfig as GlobalConfig


class TokenEncryptionController():
    EncryptionStrategy = GlobalConfig.token_encryption_strategy()

    @classmethod
    def encrypt_token(cls, func):
        """Encrypts the token string with a symmetric cryptoalgorithm"""

        @wraps(func)
        def decorated_function(*args, **kwargs):
            token: str = func(*args, **kwargs)

            return cls.EncryptionStrategy.encrypt_message(token)
        return decorated_function
    
    @classmethod
    def decrypt_token(cls, keyword: str='token'):
        """
        Decrypts the token string with a symmetric cryptoalgorithm
        
        :params str keyword: Key of KWARGS by which to look for token
        """

        def wrapper(func):
            @wraps(func)
            def decorated_function(*args, **kwargs):
                check_for_keyword_in_kwargs(kwargs, keyword, func.__name__)
                encrypted_token: str = kwargs[keyword]

                decrypted_token: str = cls.EncryptionStrategy.decrypt_message(
                    encrypted_token
                )
                kwargs[keyword] = decrypted_token

                return func(*args, **kwargs)
            return decorated_function
        return wrapper
    