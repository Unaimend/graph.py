""" """
import time


def timeit(func) -> None:
    start = time.time()
    func()
    end = time.time()
    print("Elapsed Time of", func.__name__, ":", end - start)
