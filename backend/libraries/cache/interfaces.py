"""This module provides caching interface"""


from abc import ABC, abstractmethod


class CachingStrategyInterface(ABC):
    """Provides an interface for caching strategies"""

    @abstractmethod
    def find_in_cache(self, key: str) -> str:
        """Tries to find data in cache

        :params str key: key that indentifies data in cache
        :returns str value: string that was present by provided key in the cache
        
        :raises CacheMiss: if key is not present in cache
        """

    @abstractmethod
    def write_into_cache(self, key: str, value: str) -> None:
        """Writes into cache

        :params str key: key that indentifies data in cache
        :params str value: value to store by provided key
        """

    @abstractmethod
    def delete_from_cache(self, key: str) -> None:
        """Deletes specified key from cache

        :params str key: key that indentifies data in cache
        """

class CacheControllerInterface(ABC):
    """Provides an interface for cache controller"""

    _cache_strategy: CachingStrategyInterface

    @abstractmethod
    def read_through_cache(self, keyword: str, type_: type):
        """Provides an interface to read and write data into cache while \
            reading data within nested function

        Args:
            keyword (str): key of KWARGS
            type_ (type): what object type is expected to be recieved
        """

    @abstractmethod
    def remove_from_cache(self, keyword: str):
        """Removes old data from cache

        Args:
            keyword (str): key of KWARGS
        """

    @staticmethod
    @abstractmethod
    def build():
        """Builds an instance of CacheController with current environment settings"""
