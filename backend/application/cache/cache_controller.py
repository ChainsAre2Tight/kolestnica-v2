"""This module provides a controller that oversees caching"""

from functools import wraps
from typing import Callable
import os

from utils.wrapper_checks import check_for_keyword_in_kwargs
from utils.exc import CacheMiss
from cache.cache_interface import CachingStrategyInterface
from cache.cache_strategy import *


class CacheController:
    cache_strategy: CachingStrategyInterface
    
    def __init__(self, strategy: CachingStrategyInterface):
        self.cache_strategy = strategy

    def read_through_cache(self, keyword: str, type_: type) -> Callable:
        """Provides an interface to read and write data into cache while reading data within nested function
        
        :params str keyword: key of KWARGS
        :params type type_: what object type is expected to be recieved
        """
        def wrapper(func) -> Callable:

            @wraps(func)
            def decorated_function(*args, **kwargs):
                check_for_keyword_in_kwargs(kwargs, keyword, func.__name__)
                key = kwargs[keyword]

                try:
                    result = self.cache_strategy.find_in_cache(key)
                except CacheMiss:
                    value = func(*args, **kwargs)
                    self.cache_strategy.write_into_cache(
                        key=key,
                        value=value
                    )
                    result = value
                return type_(result)
            return decorated_function
        return wrapper
        
    def remove_from_cache(self, keyword):
        """Removes old data from cache

        :params str keyword: key of KWARGS
        """
        def wrapper(func: Callable) -> Callable:
        
            @wraps(func)
            def decorated_function(*args, **kwargs):
                check_for_keyword_in_kwargs(kwargs, keyword, func.__name__)
                key = kwargs[keyword]

                self.cache_strategy.delete_from_cache(key)
            
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
                
                cache_strategy = RedisCacheStrategy(
                    redis_ = redis.Redis(
                        host=redis_url,
                        port=redis_port,
                        decode_responses=True,
                        db=redis_db,
                        # password=redis_pwd
                    )
                )
            case _:
                cache_strategy = DictCacheStrategy()
        return CacheController(cache_strategy)