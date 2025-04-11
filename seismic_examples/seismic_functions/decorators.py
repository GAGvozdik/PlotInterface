import time

def work_time(func_name='function'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"{func_name} is working ...")
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time() - start_time
            print(f"{func_name} completed in {end_time:.3f} seconds")
            return result
        return wrapper
    return decorator
import time