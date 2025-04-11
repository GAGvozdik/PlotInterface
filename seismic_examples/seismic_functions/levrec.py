import numpy as np
from .decorators import work_time

# Define the levrec function to implement the Levinson recursion algorithm
@work_time(func_name='levrec')
def levrec(r, b):
    """
    Implements the Levinson recursion algorithm.
    Args:
        r: Autocorrelation vector.
        b: Right-hand side vector.
    Returns:
        Solution vector.
    """
    n = len(r)
    a = np.zeros(n)
    a[0] = 1.0
    for k in range(1, n):
        a[k] = -np.sum(r[:k] * a[:k][::-1]) / r[0]
    return a
