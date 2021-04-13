cdef extern from "cfib.h":
    double cfibo(int n)

def fib(n):
    """Returns the nth Fibonacci number."""
    return cfibo(n)
