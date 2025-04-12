import numpy as np
from .decorators import work_time
from tqdm import tqdm

@work_time()
def gain(t, V, dt):
    """
    This function computes the gain for a given time vector and velocity.
    
    Inputs:
    t   : Time vector
    V   : Velocity
    dt  : Sampling interval
    
    Output:
    g   : Gain vector
    """
    
    GREY = "\033[90m"
    RESET = "\033[0m"
    bar_format = f"{GREY}{{l_bar}}{{bar}}{{r_bar}}{RESET}"
    
    g = np.zeros_like(t)
    for i in tqdm(range(len(t)), desc="Processing...", bar_format=bar_format):
        g[i] = (t[i] / (2 * V)) ** 2
    return g
    

