"""
This module cotains different useful functions
"""
import time

"""
param func: The function which should be executed
"""
def timeit(func, *args) -> None:
    start = time.time()
    func(*args)
    end = time.time()
    print("Elapsed Time of", func.__name__, ":", end - start)
