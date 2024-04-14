"""This module provides functions and decorators used to create and read tokens"""

import jwt
import datetime
import os

from utils.my_dataclasses import Token, SignedTokenPair
from cache.cache_controller import CacheController
from crypto.token_encryption import TokenEncryptionController


# import relevant config
Environment = os.environ.get('ENVIRONMENT') or 'TEST'
if Environment == 'TEST':
    from project_config import TestGlobalConfig as GlobalConfig
elif Environment == 'PRODUCTION':
    from project_config import ProductionGlobalConfig as GlobalConfig


class _DefaultTokenConfig:
    algorithm = 'HS256'
    secret_key = 'secret'
    access_lifetime = 300
    refresh_lifetime = 1800


class _CurrentTokenConfig(_DefaultTokenConfig):
    algorithm = GlobalConfig.token_sign_algorithm
    private_key = os.environ.get('TOKEN-SECRET-KEY') or 'very-secret-token-private-key'\
        if not GlobalConfig.overwrite_token_signature_key\
            else GlobalConfig.overwrite_token_signature_key
    public_key = os.environ.get('TOKEN-PUBLIC-KEY') or 'not-so-secret-token-public-key'\
        if not GlobalConfig.overwrite_token_verification_key\
            else GlobalConfig.overwrite_token_verification_key
    access_lifetime = GlobalConfig.access_token_lifetime
    refresh_lifetime = GlobalConfig.refresh_token_lifetime


@TokenEncryptionController.decrypt_token('raw_token')
def decode_token(raw_token: str) -> Token:
    """Decodes a token

    :params:
        str raw_token: string containing JWT token
        str algorithm: signature algorithm
        bool verify_expiration: if set to False will skip expiration check
    
    :returns dataclass.Token: dataclass Token object containing decoded token data
    """
    return Token(
        **jwt.decode(
            raw_token,
            algorithms=[_CurrentTokenConfig.algorithm],
            key=_CurrentTokenConfig.public_key
        )
    )

@TokenEncryptionController.encrypt_token
def _sign_token(token: Token) -> str:
    return jwt.encode(
        token.__dict__,
        key=_CurrentTokenConfig.secret_key,
        algorithm=_CurrentTokenConfig.algorithm
    )

@CacheController.remove_from_cache('sessionId')
def create_token_pair(sessionId: str) -> SignedTokenPair:
    """Geneartes and signs a poken pair for requesting user

    Args:
        sessionId (str): unique session fingerprint

    Returns:
        SignedTokenPair: dataclass containing tokens and their expiration time
    """
    timestamp = int(datetime.datetime.now().timestamp())
    acc_exp = timestamp + _CurrentTokenConfig.access_lifetime
    ref_exp = timestamp + _CurrentTokenConfig.refresh_lifetime

    access = Token(
        sessionId=sessionId,
        exp=acc_exp,
        typ='acc'
    )

    refresh = Token(
        sessionId=sessionId,
        exp=ref_exp,
        typ='ref'
    )

    return SignedTokenPair(
        access=_sign_token(access),
        refresh=_sign_token(refresh),
        access_expiry=acc_exp,
        refresh_expiry=ref_exp
    )
