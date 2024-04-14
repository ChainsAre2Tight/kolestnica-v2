from abc import ABC
import crypto.encryption_strategies as encryption_strategy
import cache.cache_strategy as caching_strategy
from cache.cache_interface import CachingStrategyInterface


class GlobalConfigInterface(ABC):
    token_encryption_strategy: encryption_strategy.EncryptionStrategyInterface
    json_encryption_strategy: encryption_strategy.EncryptionStrategyInterface
    database_name: str
    cache_strategy: CachingStrategyInterface


class TestGlobalConfig(GlobalConfigInterface):
    token_encryption_strategy = encryption_strategy.IdleEncryptionStrategy
    json_encryption_strategy = encryption_strategy.IdleEncryptionStrategy
    database_name = 'koleso2_test'
    cache_strategy = caching_strategy.RedisCacheStrategy


# class TestGlobalConfig(GlobalConfigInterface):
#     token_encryption_strategy = encryption_strategy.ReverseEncryptionStrategy
#     json_encryption_strategy = encryption_strategy.CaesarEncryptionStrategy
#     database_name = 'koleso2_test'
#     cache_strategy = caching_strategy.RedisCacheStrategy


class ProductionGlobalConfig(GlobalConfigInterface):
    pass