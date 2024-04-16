"""Provides a Signature class that can sign new tokens"""

import os
from jwt import encode

from utils.my_dataclasses import Token

from auth_server.services.tokens.interfaces import SignatoryIntarface


TOKEN_SIGNATURE_ALGORITHM = os.environ.get('TOKEN_SIGNATURE_ALG')
TOKEN_SIGNATURE_KEY = os.environ.get('TOKEN_SECRET_KEY')


class Signatory(SignatoryIntarface):

    @staticmethod
    def sign_token(token: Token) -> str:
        signed_token = encode(
            token.__dict__,
            key=TOKEN_SIGNATURE_KEY,
            algorithm=TOKEN_SIGNATURE_ALGORITHM
        )
        return signed_token
