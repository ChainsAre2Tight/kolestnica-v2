"""This module contains controller that oversees JSON encryption"""

import os
import json
from functools import wraps
from typing_extensions import Callable

from flask import request, Response

from libraries.utils.exc import BadEncryptionKeys

import libraries.crypto.strategies as strategy
import libraries.crypto.interfaces as interface


class JSONEncryptionController(interface.JSONEncryptionControllerInterface):

    def __init__(
            self,
            encryption_strategy: strategy.EncryptionStrategyInterface,
            decryption_key: str | int,
        ) -> None:
        self._encryption_strategy = encryption_strategy
        self._decryption_key = decryption_key

    @staticmethod
    def build():
        decryption_key = os.environ.get('JSON_PRIVATE_KEY')
        match os.environ.get('JSON_ENCRYPTION_STRATEGY'):
            case 'REVERSE':
                encryption = strategy.ReverseEncryptionStrategy
            case 'CAESAR':
                encryption = strategy.CaesarEncryptionStrategy
            case _:
                encryption = strategy.IdleEncryptionStrategy
        return JSONEncryptionController(
                encryption_strategy=encryption,
                decryption_key=decryption_key
            )

    def encrypt_json(self, provide_data: bool = False) -> Callable:
        def json_wrapper(func):
            @wraps(func)
            def json_decorated_function(*args, **kwargs):
                client_public_key: None | int | str | tuple[int, int] = None

                # if encryption requires key, check if being provided in request headers
                if self._encryption_strategy.key_format is not None:
                    try:
                        raw_key = request.headers['public-key']
                        client_public_key = self._encryption_strategy.format_key(raw_key)
                    except KeyError:
                        raise BadEncryptionKeys('Encryption key is missing')

                # decrypt payload only if its contents are necessary
                if provide_data:

                    # decrypt json payload
                    encrypted_request_data = request.get_json()
                    decrypted_request_data = self._decrypt_dict(
                        dictionary=encrypted_request_data,
                        decryption_key=self._decryption_key
                    )

                    kwargs['data'] = decrypted_request_data # decrypted_request_data

                # execute decorated function
                response: Response
                status_code: int

                response, status_code = func(*args, **kwargs)

                # encrypt json payload
                data = response.get_json()
                encrypted_response_data = self._encrypt_dict(
                    dictionary=data,
                    encryption_key=client_public_key
                )
                response.data = json.dumps(encrypted_response_data)

                return response, status_code
            return json_decorated_function
        return json_wrapper

    def _encrypt_dict(
            self,
            dictionary: dict | list,
            encryption_key: None | int | str | tuple[int, int]
        ) -> dict | list:

        if isinstance(self._encryption_strategy, strategy.IdleEncryptionStrategy):
            return dictionary

        return self._recursively_perform_action(
            iterable=dictionary,
            action=self._encryption_strategy.encrypt_message,
            key=encryption_key
        )

    def _decrypt_dict(
            self,
            dictionary: dict | list,
            decryption_key: None | int | str | tuple[int, int]
        ) -> dict | list:

        if isinstance(self._encryption_strategy, strategy.IdleEncryptionStrategy):
            return dictionary

        return self._recursively_perform_action(
            iterable=dictionary,
            action=self._encryption_strategy.decrypt_message,
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
        if isinstance(iterable, dict):
            result = {
                action(old_key, key): cls._recursively_perform_action(
                        iterable=value,
                        action=action,
                        key=key
                    )
                for old_key, value in iterable.items()
            }

        # if object is a list, iterate through values
        elif isinstance(iterable, list):
            result = [
                cls._recursively_perform_action(
                    iterable=item,
                    action=action,
                    key=key
                )
                for item in iterable
            ]

        # if object is not iterable, perform the required action against it
        elif any([isinstance(iterable, type_) for type_ in (int, str, float)]):
            result = action(iterable, key)
        else:
            raise NotImplementedError(f'Cannot encrypt/decrypt objects of type "{type(iterable)}"')
        return result
