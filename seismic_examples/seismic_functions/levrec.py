import numpy as np
from .decorators import work_time
from tqdm import tqdm

# Define the levrec function to implement the Levinson recursion algorithm
@work_time()
def levrec(r, b):
    """
    Implements the Levinson recursion algorithm.
    Args:
        r: Autocorrelation vector.
        b: Right-hand side vector.
    Returns:
        Solution vector.
    """
    
    GREY = "\033[90m"
    RESET = "\033[0m"
    bar_format = f"{GREY}{{l_bar}}{{bar}}{{r_bar}}{RESET}"
    
    n = len(r)
    a = np.zeros(n)
    a[0] = 1.0
    for k in tqdm(range(1, n), desc="Processing...", bar_format=bar_format):
        a[k] = -np.sum(r[:k] * a[:k][::-1]) / r[0]
    return a
