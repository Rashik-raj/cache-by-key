from typing import Callable

from .constants import MAX_SECONDARY_SIZE, MAX_PRIMARY_SIZE
from .data_structure.cache_class import CacheByKey


def cache_by_key(hash_arg: str | Callable = "", max_primary_size: int = MAX_PRIMARY_SIZE,
                 max_secondary_size: int = MAX_SECONDARY_SIZE):
    """
    Decorator function that enables caching by keyword argument's value for a decorated function.
    It utilizes the CacheByKey class to implement the caching behavior.

    Parameters:
        hash_arg (str): Keyword from the decorated function whose value is used for caching.
                        Default is an empty string.
                        Make sure the argument is passed as a keyword argument.
                        Make sure value of hash_arg is hashable, else cashing might not work as expected.
        max_primary_size (int): Maximum size of the cache that can uniquely cache the output of different hash_arg
                                passed to a decorated function. Default is MAX_PRIMARY_SIZE.
        max_secondary_size (int): Maximum size of each cache that can uniquely cache the output of each hash_arg
                                  passed to a decorated function. Default is MAX_SECONDARY_SIZE.

    Returns:
        A decorator function that can be used to decorate a target function.

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

    def decorating_func(decorated_func: Callable):
        return CacheByKey(decorated_func=decorated_func, hash_arg=hash_arg, max_primary_size=max_primary_size,
                          max_secondary_size=max_secondary_size)

    return decorating_func(decorated_func=hash_arg) if callable(hash_arg) else decorating_func
