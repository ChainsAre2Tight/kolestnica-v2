from utils.my_dataclasses import Token, SignedTokenPair
import jwt
import datetime

class TokenConfig:
    algorithm = 'HS256'
    secret_key = 'secret'
    access_lifetime = 300
    refresh_lifetime = 1800


def _sign_token(token: Token, config: TokenConfig) -> str:
    return jwt.encode(
        token.__dict__,
        key=config.secret_key,
        algorithm=[config.algorithm]
    )

def create_token_pair(sessionId, config: TokenConfig) -> SignedTokenPair:
    timestamp = int(datetime.datetime.now().timestamp())

    access = Token(
        sessionId=sessionId,
        exp=timestamp + config.access_lifetime,
        typ='acc'
    )

    refresh = Token(
        sessionId=sessionId,
        exp=timestamp + config.refresh_lifetime,
        typ='ref'
    )

    return SignedTokenPair(
        _sign_token(access, config),
        _sign_token(refresh, config)
    )