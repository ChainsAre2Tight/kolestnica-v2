from utils.my_dataclasses import Token, SignedTokenPair
import jwt
import datetime
from database.caching import CacheController

class DefaultTokenConfig:
    algorithm = 'HS256'
    secret_key = 'secret'
    access_lifetime = 300
    refresh_lifetime = 1800


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