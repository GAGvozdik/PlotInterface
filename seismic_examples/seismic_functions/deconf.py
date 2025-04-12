import numpy as np
from .decorators import work_time
from tqdm import tqdm

@work_time()
def deconf(R, RL, n, stab):
    """
    This function performs deconvolution using the Levinson recursion algorithm.
    
    Inputs:
    R     : Reflectivity
    RL    : Reflectivity with multiples and absorption
    n     : Number of iterations
    stab  : Stabilization factor
    
    Output:
    RASW_gain : Deconvolved reflectivity with gain applied
    """
    # Initialize variables
    N = len(R)
    RASW_gain = np.zeros(N)
    
    GREY = "\033[90m"
    RESET = "\033[0m"
    bar_format = f"{GREY}{{l_bar}}{{bar}}{{r_bar}}{RESET}"
    
    # Levinson recursion for deconvolution
    for i in tqdm(range(n), desc="Processing...", bar_format=bar_format):
        RASW_gain[i] = (R[i] - stab * RL[i]) / (1 + stab)
    
    return RASW_gain
