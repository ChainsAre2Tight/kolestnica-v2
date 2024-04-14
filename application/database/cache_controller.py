
from functools import wraps
from typing import Callable
from utils.wrapper_checks import check_for_keyword_in_kwargs
from database.cache_strategy import CacheMiss

import os

# import relevant config
Environment = os.environ.get('ENVIRONMENT') or 'TEST'
if Environment == 'TEST':
    from project_config import TestGlobalConfig as GlobalConfig
elif Environment == 'PRODUCTION':
    from project_config import ProductionGlobalConfig as GlobalConfig
        

class CacheController:
    cache_strategy = GlobalConfig.cache_strategy()

    @classmethod
    def read_through_cache(cls, keyword) -> Callable:
        """
        Provides an interface to read and write data into cache while reading data within nested function
        
        :params str keyword: key of KWARGS
        """
        def wrapper(func) -> Callable:

            @wraps(func)
            def decorated_function(*args, **kwargs):
                check_for_keyword_in_kwargs(kwargs, keyword, func.__name__)
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
                check_for_keyword_in_kwargs(kwargs, keyword, func.__name__)
                key = kwargs[keyword]

                cls.cache_strategy.delete_from_cache(key)
            
                return func(*args, **kwargs)
        
            return decorated_function
        return wrapper
    