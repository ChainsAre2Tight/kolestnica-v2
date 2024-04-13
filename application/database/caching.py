from abc import ABC, abstractmethod
from functools import wraps, partial
from typing import Callable

data = dict()

class CacheMiss(BaseException):
    """Raised when requested key does not exist in key"""

class CachingInterface(ABC):

    @staticmethod
    @abstractmethod
    def find_in_cache(key: str) -> str:
        """
        Tries to find data in cache

        :params str key: key that indentifies data in cache
        :returns str value: string that was present by provided key in the cache
        
        :raises CacheMiss: if key is not present in cache
        """
        pass

    
    @staticmethod
    @abstractmethod
    def write_into_cache(key: str, value: str) -> None:
        """
        Writes into cache

        :params str key: key that indentifies data in cache
        :params str value: value to store by provided key
        """
        pass

class DictCache(CachingInterface):

    @staticmethod
    def find_in_cache(key: str) -> str:
        try:
            value = data[key]
            print(f'Read {value} by {key}')
            return value
        except KeyError:
            print(f'Could not find value by {key}')
            raise CacheMiss(f'Could not find data for key "{key}"')
    
    @staticmethod
    def write_into_cache(key: str, value: str):
        print(f'Wrote {value} into {key}')
        data[key] = value

class RedisCache(CachingInterface):

    @staticmethod
    def find_in_cache(key: str) -> str:
        raise NotImplementedError
    
    @staticmethod
    def write_into_cache(key: str, value: str) -> None:
        raise NotImplementedError

def read_through_cache(func) -> Callable | str:
    """
    Provides an interface to read and write data into cache while reading data within nested function
    """
    cache_strategy = DictCache
    
    @wraps(func)
    def decorated_function(key, *args, **kwargs):
        try:
            return cache_strategy.find_in_cache(key)
        except CacheMiss:
            value = func(key, *args, **kwargs)
            cache_strategy.write_into_cache(
                key=key,
                value=value
            )
            return value
    
    return decorated_function