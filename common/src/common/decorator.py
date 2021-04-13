import time


def timeit(f):
    def run(*args, **kwargs):
        begin = time.time()
        result = f(*args, **kwargs)
        print(f"Time elapsed for function {f.__name__}: {time.time() - begin}")
        return result
    return run
