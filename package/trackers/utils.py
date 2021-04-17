import time


def retry(func=None, *, tries=3, timeout=0.0):
    def decorator(_func):
        def inner(*args, **kwargs):
            for n in range(1, tries + 1):
                try:
                    return _func(*args, **kwargs)
                except Exception:
                    if n == tries:
                        raise
                if timeout:
                    time.sleep(timeout)
        return inner
    return decorator(func) if func else decorator
