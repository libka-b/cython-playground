from common.decorator import timeit

from wrap_fib import fib


@timeit
def fibo_py(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = a + b, a
    return a


if __name__ == "__main__":
    fibo_py(1000)
    timeit(fib)(1000)
