import time
from functools import wraps


def message_and_time(message: str = ''):
    """Decorator to print a message and the elapsed time of a function."""
    def decorated(func: callable):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if message != '':
                print(message)
            print(f'{func.__name__}...', end='')
            st = time.perf_counter()
            results = func(*args, **kwargs)
            print(f"{time.perf_counter() - st:.1f}s")
            return results
        return wrapped
    return decorated
