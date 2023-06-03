import hashlib
from functools import update_wrapper
from typing import Any, Callable

from ..constants import MAX_PRIMARY_SIZE, MAX_SECONDARY_SIZE, MIN_SECONDARY_SIZE, MIN_PRIMARY_SIZE
from ..data_structure import DequeCacheDict


class CacheByKey:
    """
        Implements LRU cache which supports caching by keyword argument's value.
        On top of it, each keyword argument's cache can have at most 10 different LRU caches.

        Parameters:
            hash_arg (str): Keyword from the decorated function whose value is used for caching.
                        Default is an empty string.
                        Make sure the argument is passed as a keyword argument.
                        Make sure value of hash_arg is hashable, else cashing might not work as expected.
            max_primary_size (int): Maximum size of the cache that can uniquely cache the output of different hash_arg
                                    passed to a decorated function. Default is MAX_PRIMARY_SIZE.
            max_secondary_size (int): Maximum size of each cache that can uniquely cache the output of each hash_arg
                                      passed to a decorated function. Default is MAX_SECONDARY_SIZE.

        Methods:
            cache_info(): Retrieves information about the cache for the decorated function.
            clear_cache(): Clears the entire cache for the decorated function.
            remove_cache(hash_arg_value): Removes the cache for a specific hash_arg value.

        Example:
            @CacheByKey(max_primary_size=5, max_secondary_size=3, hash_arg="n")
            def fib(n: int):
                if n <= 1:
                    return n
                return fib(n=n - 1) + fib(n=n - 2)

            fib(n=10)
            fib(n=12)
            print(fib.cache_info())

            Output:
            {
                'cache_len': 5,
                'max_primary_size': 5,
                'max_secondary_size': 3,
                'cache_hit': 3,
                'cache_miss': 13
            }

            fib.remove_cache(11)
            print(fib.cache_info())

            Output:
            {
                'cache_len': 4,
                'max_primary_size': 5,
                'max_secondary_size': 3,
                'cache_hit': 3,
                'cache_miss': 13
            }

            fib.clear_cache()
            print(fib.cache_info())

            Output:
            {
                'cache_len': 0,
                'max_primary_size': 5,
                'max_secondary_size': 3,
                'cache_hit': 0,
                'cache_miss': 0
            }
        """

    def __init__(
            self,
            decorated_func: Callable,
            hash_arg: str = "",
            max_primary_size: int = MAX_PRIMARY_SIZE,
            max_secondary_size: int = MAX_SECONDARY_SIZE,
    ) -> None:
        if max_secondary_size > MAX_SECONDARY_SIZE:
            max_secondary_size = MAX_SECONDARY_SIZE
        elif max_secondary_size < MIN_SECONDARY_SIZE:
            max_secondary_size = MIN_SECONDARY_SIZE

        if max_primary_size > MAX_PRIMARY_SIZE:
            max_primary_size = MAX_PRIMARY_SIZE
        elif max_primary_size < MIN_PRIMARY_SIZE:
            max_primary_size = MIN_PRIMARY_SIZE

        self.method = decorated_func
        self.max_primary_size: int = max_primary_size
        self.max_secondary_size: int = max_secondary_size
        self.__cache: DequeCacheDict = DequeCacheDict(max_size=max_primary_size)
        self.hit: int = 0
        self.miss: int = 0
        self.hash_arg: str = hash_arg
        update_wrapper(self, decorated_func)

    def __call__(self, *args, **kwargs) -> Any:
        primary_key = kwargs.get(self.hash_arg, "no-key")
        primary_key = self.__get_hashable_primary_key(primary_key=primary_key)
        secondary_key = self.__get_method_hash(*args, **kwargs)
        result = self.__get_cache_data(primary_key=primary_key, secondary_key=secondary_key)
        if result is None:
            result = self.method(*args, **kwargs)
            self.__update_cache(primary_key=primary_key, secondary_key=secondary_key, value=result)
            self.miss += 1
        else:
            self.hit += 1
        return result

    def __update_cache(self, primary_key: Any, secondary_key: str, value: Any) -> None:
        if primary_key not in self.__cache:
            cache_data = DequeCacheDict(max_size=self.max_secondary_size)
            cache_data[secondary_key] = value
            self.__cache[primary_key] = cache_data
        else:
            self.__cache[primary_key][secondary_key] = value

    @staticmethod
    def __get_hashable_primary_key(primary_key: Any):
        try:
            hash(primary_key)
            return primary_key
        except TypeError:
            return str(primary_key)

    @staticmethod
    def __get_method_hash(*args, **kwargs) -> str:
        return hashlib.sha224((str(args) + str(kwargs)).encode()).hexdigest()

    def __get_cache_length(self) -> int:
        return self.__cache.__len__()

    def __get_cache_data(self, primary_key: Any, secondary_key: str) -> Any:
        _temp = self.__cache.get(primary_key)
        if _temp is not None:
            return _temp.get(secondary_key)

    def cache_info(self) -> dict:
        """
        returns the info about current instance of cache.
        """
        return {
            "cache_len": self.__get_cache_length(),
            "max_primary_size": self.max_primary_size,
            "max_secondary_size": self.max_secondary_size,
            "cache_hit": self.hit,
            "cache_miss": self.miss,
        }

    def clear_cache(self) -> None:
        """
        clears out all the cache.
        """
        self.__cache.clear()
        self.hit = 0
        self.miss = 0

    def remove_cache(self, hash_arg_value: Any):
        """
        removes cache for selected hash_arg_value.
        """
        if hash_arg_value in self.__cache:
            del self.__cache[hash_arg_value]
            del self.__cache[hash_arg_value]
