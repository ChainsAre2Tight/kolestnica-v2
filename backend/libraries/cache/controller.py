"""This module provides a controller that oversees caching"""

from typing import Callable
import os

from libraries.utils.wrapper_checks import check_for_keyword_in_kwargs
from libraries.utils.exc import CacheMiss
import libraries.cache.interfaces as interface
import libraries.cache.strategies as strategy


class CacheController(interface.CacheControllerInterface):
    """Provides decorators for cache interactions"""

    def __init__(self, cache_strategy: interface.CachingStrategyInterface):
        self._cache_strategy = cache_strategy

    def read_through_cache(self, keyword: str, type_: type):
        def wrapper(func):
            def decorated_function(*args, **kwargs):
                check_for_keyword_in_kwargs(kwargs, keyword, func.__name__)
                key = kwargs[keyword]

                try:
                    result = self._cache_strategy.find_in_cache(key)
                except CacheMiss:
                    value = func(*args, **kwargs)
                    self._cache_strategy.write_into_cache(
                        key=key,
                        value=value
                    )
                    result = value
                return type_(result)
            return decorated_function
        return wrapper

    def remove_from_cache(self, keyword):
        def wrapper(func: Callable) -> Callable:
            def decorated_function(*args, **kwargs):
                check_for_keyword_in_kwargs(kwargs, keyword, func.__name__)
                key = kwargs[keyword]

                self._cache_strategy.delete_from_cache(key)

                return func(*args, **kwargs)
            return decorated_function
        return wrapper

    @staticmethod
    def build():
        match os.environ.get('CACHE_STRATEGY'):
            case 'REDIS':
                import redis

                redis_url = os.environ.get('REDIS_HOST')
                redis_port = int(os.environ.get('REDIS_PORT') or 6379)
                redis_db = int(os.environ.get('REDIS_SESSION_DB') or 0)
                # redis_pwd = os.environ.get('REDIS_PASSWORD')

                cache_strategy = strategy.RedisCacheStrategy(
                    redis_ = redis.Redis(
                        host=redis_url,
                        port=redis_port,
                        decode_responses=True,
                        db=redis_db,
                        # password=redis_pwd
                    )
                )
            case _:
                cache_strategy = strategy.DictCacheStrategy()
        return CacheController(cache_strategy)
