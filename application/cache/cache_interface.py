from abc import ABC, abstractmethod


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