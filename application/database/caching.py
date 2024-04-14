from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable

import redis

data = dict()

class CacheMiss(BaseException):
    """Raised when requested key does not exist in key"""

class CachingStrategyInterface(ABC):

    @abstractmethod
    def find_in_cache(self, key: str) -> str:
        """
        Tries to find data in cache

        :params str key: key that indentifies data in cache
        :returns str value: string that was present by provided key in the cache
        
        :raises CacheMiss: if key is not present in cache
        """
        pass

    
    @abstractmethod
    def write_into_cache(self, key: str, value: str) -> None:
        """
        Writes into cache

        :params str key: key that indentifies data in cache
        :params str value: value to store by provided key
        """
        pass

    @abstractmethod
    def delete_from_cache(self, key: str) -> None:
        """
        Deletes specified key from cache

        :params str key: key that indentifies data in cache
        """
        pass

class DictCacheStrategy(CachingStrategyInterface):
    
    def __init__(self):
        self.data = dict()

    def find_in_cache(self, key: str) -> str:
        try:
            return self.data[key]
        except KeyError:
            raise CacheMiss(f'Could not find data for key "{key}"')

    def write_into_cache(self, key: str, value: str):
        print(f'Wrote {value} into {key}')
        data[key] = value
    
    def delete_from_cache(self, key: str) -> None:
        try:
            self.data.pop(key)
        except KeyError:
            pass # ignore

class RedisCacheStrategy(CachingStrategyInterface):
    debug = True

    def __init__(self):
        self.r = redis.Redis(decode_responses=True)
        
        if self.debug:
            print(f'---> Redis is alivable ({self.r.ping()})')

    def find_in_cache(self, key: str) -> str:
        value = self.r.get(key)

        if value is not None:
            if self.debug:
                print(f'Read value ({value}) by ({key})')
            return value
        else:
            if self.debug:
                print(f'Could not read value by ({key})')
            raise CacheMiss(f'Could not find data for key "{key}"')
    
    def write_into_cache(self, key: str, value: str) -> None:
        self.r.set(key, value)
        if self.debug:
            print(f'Set value ({value}) by key ({key})')
       
    
    def delete_from_cache(self, key: str) -> None:
        self.r.delete(key)
        if self.debug:
            print(f'Deleted key "{key}" from cache')
        

class CacheController:
    cache_strategy = RedisCacheStrategy()

    @classmethod
    def read_through_cache(cls, keyword) -> Callable:
        """
        Provides an interface to read and write data into cache while reading data within nested function
        
        :params str keyword: key of KWARGS
        """
        def wrapper(func) -> Callable:

            @wraps(func)
            def decorated_function(*args, **kwargs):
                assert keyword in kwargs.keys(), f'Keyword "{keyword}" is missing in kwargs of {func.__name__}'
                key = kwargs[keyword]

                try:
                    return cls.cache_strategy.find_in_cache(key)
                except CacheMiss:
                    value = func(*args, **kwargs)
                    cls.cache_strategy.write_into_cache(
                        key=key,
                        value=value
                    )
                    return value
            
            return decorated_function
        return wrapper
        
    @classmethod
    def remove_from_cache(cls, keyword):
        """
        Removes old data from cache

        :params str keyword: key of KWARGS
        """
        def wrapper(func: Callable) -> Callable:
        
            @wraps(func)
            def decorated_function(*args, **kwargs):
                assert keyword in kwargs.keys(), f'Keyword "{keyword}" is missing in kwargs of {func.__name__}'
                key = kwargs[keyword]

                cls.cache_strategy.delete_from_cache(key)
            
                return func(*args, **kwargs)
        
            return decorated_function
        return wrapper
    