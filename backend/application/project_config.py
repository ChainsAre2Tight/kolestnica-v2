"""This module provides global configs that determine strategies used in the project"""

from abc import ABC
from typing_extensions import Literal

import crypto.encryption_strategies as encryption_strategy
import cache.cache_strategy as caching_strategy
from cache.cache_interface import CachingStrategyInterface


class GlobalConfigInterface(ABC):
    database_name: str
    
    token_encryption_strategy: encryption_strategy.EncryptionStrategyInterface
    json_encryption_strategy: encryption_strategy.EncryptionStrategyInterface
    cache_strategy: CachingStrategyInterface
    
    token_sign_algorithm: Literal['HS256', 'RS256']
    overwrite_token_verification_key: str | bool = False
    overwrite_token_signature_key: str | bool = False
    access_token_lifetime: int
    refresh_token_lifetime: int


class TestGlobalConfig(GlobalConfigInterface):
    database_name = 'koleso2_test'
    
    token_encryption_strategy = encryption_strategy.IdleEncryptionStrategy
    json_encryption_strategy = encryption_strategy.IdleEncryptionStrategy
    cache_strategy = caching_strategy.DictCacheStrategy
    
    token_sign_algorithm = 'HS256'
    overwrite_token_verification_key = 'secret'
    overwrite_token_signature_key = 'secret'
    access_token_lifetime = 30
    refresh_token_lifetime = 180


# class TestGlobalConfig(GlobalConfigInterface):
#     database_name = 'koleso2_test'
    
#     token_encryption_strategy = encryption_strategy.ReverseEncryptionStrategy
#     json_encryption_strategy = encryption_strategy.CaesarEncryptionStrategy
#     cache_strategy = caching_strategy.RedisCacheStrategy
    
#     token_sign_algorithm = 'HS256'
#     overwrite_token_verification_key = 'secret'
#     overwrite_token_signature_key = 'secret'
#     access_token_lifetime = 30
#     refresh_token_lifetime = 180


class ProductionGlobalConfig(GlobalConfigInterface):
    database_name = 'koleso2_production'
    
    token_encryption_strategy = encryption_strategy.ReverseEncryptionStrategy
    json_encryption_strategy = encryption_strategy.CaesarEncryptionStrategy
    cache_strategy = caching_strategy.RedisCacheStrategy
    
    token_sign_algorithm = 'RS256'
    access_token_lifetime: 300
    refresh_token_lifetime: 1800