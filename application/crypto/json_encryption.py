from crypto.encryption_strategies import *
from functools import wraps
from typing_extensions import Callable
from flask import request, Response
import json
from abc import ABC, abstractmethod
import os

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
        pass


class JSONEncryptionController(JSONEncryptionControllerInterface):    
    _encryption_strategy = GlobalConfig.json_encryption_strategy()
    
    @classmethod
    def encrypt_json(cls, provide_data: bool = False) -> Callable:
        def wrapper(func):
            @wraps(func)
            def decorated_function(*args, **kwargs):
                # if there is no need to decrypt payload, skip decryption
                if provide_data:
                    
                    # decrypt json payload
                    encrypted_request_data = request.get_json()
                    decrypted_request_data = cls._decrypt_dict(encrypted_request_data)

                    kwargs['data'] = decrypted_request_data
                
                # perform handler function
                response: Response
                status_code: int

                response, status_code = func(*args, **kwargs)

                # ecnrypt json payload
                data = response.get_json()
                encrypted_response_data = cls._encrypt_dict(data)
                response.data = json.dumps(encrypted_response_data)

                return response, status_code
            
            return decorated_function
        return wrapper
    
    @classmethod
    def _encrypt_dict(cls, dictionary: dict | list) -> dict | list:
        return cls._recursively_perform_action(
            iterable=dictionary,
            action=cls._encryption_strategy.encrypt_message
        )
    
    @classmethod
    def _decrypt_dict(cls, dictionary: dict | list) -> dict | list:
        return cls._recursively_perform_action(
            iterable=dictionary,
            action=cls._encryption_strategy.decrypt_message
        )

    @classmethod
    def _recursively_perform_action(
            cls,
            iterable: dict | list | str | int,
            action: Callable
        ) -> dict | list | str:
        

        # if object is a dictionary, iterate through keys and values
        if type(iterable) is dict:
            result = {
                action(key): cls._recursively_perform_action(
                    iterable=value,
                    action=action
                )
                for key, value in iterable.items()
            }

            for old_key, old_value in iterable.items():
                new_key = action(old_key)
                
                new_value = action(old_value)
                
                result[new_key] = new_value
        
        elif type(iterable) is list:
            result = [
                cls._recursively_perform_action(
                    iterable=item,
                    action=action
                )
                for item in iterable
            ]
        else:
            result = action(iterable)
        
        return result
    