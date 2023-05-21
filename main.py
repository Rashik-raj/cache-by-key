from src.cache_by_key.cache_utils import cache_by_key


@cache_by_key(hash_arg="n", max_primary_size=3, max_secondary_size=1)
def fib(n: int):
    return n if n <= 1 else fib(n=n - 1) + fib(n=n - 2)


if __name__ == "__main__":
    from time import time

    t1 = time()
    print(fib(n=100))
    t2 = time()
    print("time taken for using first cache", t2 - t1)
    print(fib(n=100))
    t3 = time()
    print("time taken for using second cache", t3 - t2)
    print(fib.cache_info())
