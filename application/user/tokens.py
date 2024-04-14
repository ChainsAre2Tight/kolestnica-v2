from utils.my_dataclasses import Token, SignedTokenPair
import jwt
import datetime
from database.cache_controller import CacheController
from typing_extensions import Literal
import os
from crypto.token_encryption import TokenEncryptionController

class DefaultTokenConfig:
    algorithm = 'HS256'
    secret_key = 'secret'
    access_lifetime = 300
    refresh_lifetime = 1800

TokenPublicKey = os.environ.get('TOKEN-PUBLIC-KEY') or 'secret'

@TokenEncryptionController.decrypt_token('raw_token')
def decode_token(
        raw_token: str,
        algorithm: Literal['HS256', 'RS256'] = 'HS256',
        verify_expiration: bool = True
    ) -> Token:
    """
    Decodes a token

    :params:
        str raw_token: string containing JWT token
        str algorithm: signature algorithm
        bool verify_expiration: if set to False will skip expiration check
    
    :returns dataclass.Token: dataclass Token object containing decoded token data
    """
    return Token(
        **jwt.decode(
            raw_token,
            algorithms=[algorithm],
            options={'verify_exp': verify_expiration},
            key=TokenPublicKey
        )
    )

@TokenEncryptionController.encrypt_token
def _sign_token(token: Token, config: DefaultTokenConfig) -> str:
    return jwt.encode(
        token.__dict__,
        key=config.secret_key,
        algorithm=config.algorithm
    )

@CacheController.remove_from_cache('sessionId')
def create_token_pair(sessionId: str, config: DefaultTokenConfig) -> SignedTokenPair:
    timestamp = int(datetime.datetime.now().timestamp())
    acc_exp = timestamp + config.access_lifetime
    ref_exp = timestamp + config.refresh_lifetime

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
        access=_sign_token(access, config),
        refresh=_sign_token(refresh, config),
        access_expiry=acc_exp,
        refresh_expiry=ref_exp
    )
