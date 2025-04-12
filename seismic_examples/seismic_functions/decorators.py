import time

def work_time():
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"{func.__name__} is working ...")
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time() - start_time
            print(f"{func.__name__} completed in {end_time:.3f} seconds")
            return result
        return wrapper
    return decorator
