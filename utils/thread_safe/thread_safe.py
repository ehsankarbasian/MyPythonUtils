from functools import wraps
from threading import RLock


def thread_safe(func):
    
    _lock: RLock = RLock()
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        with _lock:
            return func(*args, **kwargs)
    return wrapper
