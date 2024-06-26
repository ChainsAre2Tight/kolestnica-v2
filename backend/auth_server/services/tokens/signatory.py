"""Provides a Signature class that can sign new tokens"""

import os
from jwt import encode

from libraries.utils.my_dataclasses import Token
from libraries.crypto import token_encryptor

from auth_server.services.tokens.interfaces import SignatoryIntarface


TOKEN_SIGNATURE_ALGORITHM = os.environ.get('TOKEN_SIGNATURE_ALG')
TOKEN_SIGNATURE_KEY = os.environ.get('TOKEN_SECRET_KEY')

if TOKEN_SIGNATURE_ALGORITHM == 'RS256':
    raw_key = os.environ.get('TOKEN_SECRET_KEY').replace(r'\\n', '\n')
    TOKEN_SIGNATURE_KEY = bytes(raw_key, 'utf-8')


class Signatory(SignatoryIntarface):

    @staticmethod
    @token_encryptor.encrypt_token
    def sign_token(token: Token) -> str:
        signed_token = encode(
            token.__dict__,
            key=TOKEN_SIGNATURE_KEY,
            algorithm=TOKEN_SIGNATURE_ALGORITHM
        )
        return signed_token
