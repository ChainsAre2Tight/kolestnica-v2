"""This module provides caching strategies

Alivable strategies:
- DictCache: uses Python dictionary
- RedisCache: uses a Redis instance
"""

from cache.cache_interface import CachingStrategyInterface
from utils.exc import CacheMiss


class DictCacheStrategy(CachingStrategyInterface):
    """Uses a Python dictionary as its storage"""
    
    def __init__(self):
        self.data = dict()

    def find_in_cache(self, key: str) -> str:
        try:
            return self.data[key]
        except KeyError:
            raise CacheMiss(f'Could not find data for key "{key}"')

    def write_into_cache(self, key: str, value: str):
        print(f'Wrote {value} into {key}')
        self.data[key] = value
    
    def delete_from_cache(self, key: str) -> None:
        try:
            self.data.pop(key)
        except KeyError:
            pass # ignore


class RedisCacheStrategy(CachingStrategyInterface):
    """Uses a Redis instance as its storage"""
    debug = True

    def __init__(self, redis_):
        self.r = redis_
        
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
