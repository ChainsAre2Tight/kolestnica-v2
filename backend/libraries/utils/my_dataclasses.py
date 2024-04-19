"""Provides various dataclasses used throught this project"""


from dataclasses import dataclass
from typing_extensions import Literal


@dataclass
class Token:
    sessionId: str
    exp: int
    typ: Literal['acc', 'ref']


@dataclass
class SignedTokenPair:
    access: str
    refresh: str
    access_expiry: int
    refresh_expiry: int
