import numpy as np
from .decorators import work_time

@work_time(func_name='deconf')
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
    
    # Levinson recursion for deconvolution
    for i in range(n):
        RASW_gain[i] = (R[i] - stab * RL[i]) / (1 + stab)
    
    return RASW_gain
