import time
import pickle
from functools import wraps

def logtime(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        total = time.perf_counter() - start
        print(f'{func.__name__} took {total} sec to run.')
        return result
    return wrapper

@logtime
def test(something='abc'):
    """ Something doc. """
    pass

test()

def once_per_minute(func):
    last_invoked = 0
    def wrapper(*args, **kwargs):
        nonlocal last_invoked
        elapsed_time = time.perf_counter() - last_invoked
        if elapsed_time < 60:
            raise RuntimeError('Call too often')
        last_invoked = time.perf_counter()
        return func(*args, **kwargs)
    return wrapper


@once_per_minute
def test2(something='abc'):
    """ Something doc. """
    pass

test2()
test2()

def once_per_n(n):
    def second_wrapper(func):
        last_invoked = 0
        def wrapper(*args, **kwargs):
            nonlocal last_invoked
            elapsed_time = time.perf_counter() - last_invoked
            if elapsed_time < n:
                raise RuntimeError('Call too often')
            last_invoked = time.perf_counter()
            return func(*args, **kwargs)
        return wrapper
    return second_wrapper

def memoize(func):
    cache = {}
    def wrapper(*args, **kwargs):
        t = (pickle.dumps(args), pickle.dumps(kwargs))
        if t not in cache:
            print(f'Caching {func.__name__}')
            cache[t] = func(*args, **args)
        else:
            print(f'Using old value {func.__name__}')
        return cache[t]
    return wrapper

def object_birthday(cls):
    cls.__repr__ = 'fancy_repr'
    def wrapper(*args, **kwargs):
        ins = cls(*args, **kwargs)
        ins._create_at = time.time()
        return ins
    return wrapper

def create_decorator(argument):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            funny_stuff()
            something_with_argument(argument)
            retval = function(*args, **kwargs)
            more_funny_stuff()
            return retval
        return wrapper
    return decorator


@create_decorator
def test3():
    pass

test3()