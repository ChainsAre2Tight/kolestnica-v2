from database.cache_interface import CachingStrategyInterface
import redis

class CacheMiss(BaseException):
    """Raised when requested key does not exist in key"""


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
        self.data[key] = value
    
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