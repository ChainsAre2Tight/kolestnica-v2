"""Provides a token creator class that creates new tokens"""

import os
from datetime import datetime

from utils.my_dataclasses import SignedTokenPair, Token

from auth_server.services.tokens.interfaces import TokenPairCreatorIntarface
from auth_server.services.tokens.signatory import Signatory


ACCESS_TOKEN_EXPIRY: int = int(os.environ.get('ACCESS_LIFETIME') or 300)
REFRESH_TOKEN_EXPIRY: int = int(os.environ.get('REFRESH_LIFETIME') or 1800)


class TokenPairCreator(TokenPairCreatorIntarface):

    @staticmethod
    def create(browser_fingerprint: str) -> SignedTokenPair:
        timestamp = int(datetime.now().timestamp())

        # create tokens
        access_token = TokenPairCreator._create_acess_token(
                timestamp=timestamp,
                browser_fingerprint=browser_fingerprint
            )
        refresh_token = TokenPairCreator._create_refresh_token(
                timestamp=timestamp,
                browser_fingerprint=browser_fingerprint
            )

        # use signatory to sign them
        signed_access_token = Signatory.sign_token(access_token)
        signed_refresh_token = Signatory.sign_token(refresh_token)

        signed_token_pair = SignedTokenPair(
            access=signed_access_token,
            refresh=signed_refresh_token,
            access_expiry=access_token.exp,
            refresh_expiry=refresh_token.exp
        )
        return signed_token_pair

    @staticmethod
    def _create_acess_token(timestamp, browser_fingerprint: str) -> Token:
        access_token = Token(
            sessionId=browser_fingerprint,
            exp=timestamp + ACCESS_TOKEN_EXPIRY,
            typ='acc'
        )
        return access_token

    @staticmethod
    def _create_refresh_token(timestamp, browser_fingerprint: str) -> Token:
        refresh_token = Token(
            sessionId=browser_fingerprint,
            exp=timestamp + REFRESH_TOKEN_EXPIRY,
            typ='ref'
        )
        return refresh_token
