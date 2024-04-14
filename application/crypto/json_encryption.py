"""This module contains controller that oversees JSON encryption"""

from flask import request, Response
from functools import wraps
from abc import ABC, abstractmethod
from typing_extensions import Callable
import json
import os

from crypto.encryption_strategies import *
from utils.exc import BadEncryptionKeys

# import relevant config
Environment = os.environ.get('ENVIRONMENT') or 'TEST'
if Environment == 'TEST':
    from project_config import TestGlobalConfig as GlobalConfig
elif Environment == 'PRODUCTION':
    from project_config import ProductionGlobalConfig as GlobalConfig


class JSONEncryptionControllerInterface(ABC):
    _encryption_strategy: EncryptionStrategyInterface

    @classmethod
    @abstractmethod
    def encrypt_json(cls, provide_data: bool = False) -> Callable:
        """A decorator that will encrypt and decrypt json of decorated requests

        Args:
            provide_data (bool, optional): If set to True will provide "data" attribute\
        to decorated functions containing decrypted JSON data. Defaults to False.

        Raises:
            BadEncryptionKeys: If header containing keys is missing or keys are in wrong format
            NotImplementedError: If JSON contains data that cannot be encrypted
        """


class JSONEncryptionController(JSONEncryptionControllerInterface):    
    _encryption_strategy = GlobalConfig.json_encryption_strategy
    
    @classmethod
    def encrypt_json(cls, provide_data: bool = False) -> Callable:
        def wrapper(func):
            @wraps(func)
            def decorated_function(*args, **kwargs):
                key: None | int | str | tuple[int, int] = None
                
                # if encryption requires key, check if being provided in request headers
                if cls._encryption_strategy.key_format is not None:
                    try:
                        raw_key = request.headers['enc-key']
                        key = cls._encryption_strategy.format_key(raw_key)
                        print('key is', key)
                    except KeyError:
                        raise BadEncryptionKeys('Encryption key is missing')
                    
                # decrypt payload only if its contents are necessary
                if provide_data:
                    
                    # decrypt json payload
                    encrypted_request_data = request.get_json()
                    decrypted_request_data = cls._decrypt_dict(
                        dictionary=encrypted_request_data,
                        decryption_key=key
                    )

                    kwargs['data'] = decrypted_request_data
                
                # execute decorated function
                response: Response
                status_code: int

                response, status_code = func(*args, **kwargs)

                # encrypt json payload
                data = response.get_json()
                encrypted_response_data = cls._encrypt_dict(
                    dictionary=data,
                    encryption_key=key
                )
                response.data = json.dumps(encrypted_response_data)

                return response, status_code
            
            return decorated_function
        return wrapper
    
    @classmethod
    def _encrypt_dict(
            cls,
            dictionary: dict | list,
            encryption_key: None | int | str | tuple[int, int]
        ) -> dict | list:
        
        return cls._recursively_perform_action(
            iterable=dictionary,
            action=cls._encryption_strategy.encrypt_message,
            key=encryption_key
        )
    
    @classmethod
    def _decrypt_dict(
            cls,
            dictionary: dict | list,
            decryption_key: None | int | str | tuple[int, int]
        ) -> dict | list:
        
        return cls._recursively_perform_action(
            iterable=dictionary,
            action=cls._encryption_strategy.decrypt_message,
            key=decryption_key
        )

    @classmethod
    def _recursively_perform_action(
            cls,
            iterable: dict | list | str | int,
            action: Callable,
            key: None | str | int | tuple[int, int]
        ) -> dict | list | str:
        
        # if object is a dictionary, iterate through keys and values
        if type(iterable) is dict:
            result = {
                action(old_key, key): cls._recursively_perform_action(
                        iterable=value,
                        action=action,
                        key=key
                    )
                for old_key, value in iterable.items()
            }
        
        # if object is a list, iterate through values
        elif type(iterable) is list:
            result = [
                cls._recursively_perform_action(
                    iterable=item,
                    action=action,
                    key=key
                )
                for item in iterable
            ]
        
        # if object is not iterable, perform the required action against it
        elif type(iterable) is int or str or float:
            result = action(iterable, key)
        else:
            raise NotImplementedError(f'Cannot encrypt/decrypt objects of type "{type(iterable)}"')
        return result
    