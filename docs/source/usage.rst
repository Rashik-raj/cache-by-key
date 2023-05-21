Usage
=====

Caching
-------

- Using minimalistic cache_by_key decorator

.. code-block:: python
   :linenos:

    from cache_by_key.cache_utils import cache_by_key

    @cache_by_key
    def fib(n: int):
        return n if n <= 1 else fib(n=n - 1) + fib(n=n - 2)

    fib(100)

- Using hash_arg key in cache_by_key decorator

.. code-block:: python
   :linenos:

    from cache_by_key.cache_utils import cache_by_key

    @cache_by_key(hash_arg="n")
    def fib(n: int):
        return n if n <= 1 else fib(n=n - 1) + fib(n=n - 2)

    fib(n=100)

**Notice that value of hash_arg is the name of the keyword. And we also should pass the value using keyword when calling a function.**

- Controlling the cache size

.. code-block:: python
   :linenos:

    from cache_by_key.cache_utils import cache_by_key

    @cache_by_key(hash_arg="n", max_primary_size=3, max_secondary_size=1)
    def fib(n: int):
        return n if n <= 1 else fib(n=n - 1) + fib(n=n - 2)

    fib(n=100)

**Here we have set max_primary_size to 3, and hence limit the cache size to 3 for unique value of n, removing old cache automatically in FIFO (First In First Out) fashion.**

**Also max_secondary_size is set to 1 because we only have one parameter. If there had been other parameter along side n, then for each value of n, we can cache different variation of other parameter using secondary cache.**

View cache info
---------------
**This will return the cache info as a dictionary containing "cache_len", "max_primary_size", "max_secondary_size", "cache_hit" and "cache_miss".**

.. code-block:: python
    :linenos:

    print(fib.cache_info())

Remove certain cache
--------------------
**This will remove cache for fib function having n=10.**

.. code-block:: python
    :linenos:

    fib.remove_cache(hash_arg_value=10)

Clearing the cache
------------------
**This will clear all the cache for fib function.**

.. code-block:: python
    :linenos:

    fib.clear_cache()
