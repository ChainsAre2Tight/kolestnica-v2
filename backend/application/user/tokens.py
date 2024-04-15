"""This module provides functions and decorators used to create and read tokens"""

import jwt
import datetime
import os

from utils.my_dataclasses import Token, SignedTokenPair
from cache.cache_controller import CacheController
from crypto.token_encryption import TokenEncryptionController
import crypto.encryption_strategies as enc_strat


class _TokenConfig:
    algorithm = os.environ.get('TOKEN_SIGNATURE_ALG')
    public_key = os.environ.get('TOKEN_PUBLIC_KEY')
    secret_key = os.environ.get('TOKEN_SECRET_KEY')
    access_lifetime = int(os.environ.get('ACCESS_LIFETIME') or 300)
    refresh_lifetime = int(os.environ.get('REFRESH_LIFETIME') or 1800)


match os.environ.get('TOKEN_ENCRYPTION_STRATEGY'):
    case 'IDLE':
        encryption = enc_strat.IdleEncryptionStrategy
    case 'REVERSE':
        encryption = enc_strat.ReverseEncryptionStrategy
    case 'CAESAR':
        encryption = enc_strat.CaesarEncryptionStrategy
    case _:
        encryption = enc_strat.IdleEncryptionStrategy

token_encryption = TokenEncryptionController(
    encryption=encryption
)


@token_encryption.decrypt_token('raw_token')
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
            algorithms=[_TokenConfig.algorithm],
            key=_TokenConfig.public_key
        )
    )

@token_encryption.encrypt_token
def _sign_token(token: Token) -> str:
    return jwt.encode(
        token.__dict__,
        key=_TokenConfig.secret_key,
        algorithm=_TokenConfig.algorithm
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
    acc_exp = timestamp + _TokenConfig.access_lifetime
    ref_exp = timestamp + _TokenConfig.refresh_lifetime

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
