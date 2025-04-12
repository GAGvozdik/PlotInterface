import numpy as np
from .decorators import work_time
from tqdm import tqdm

@work_time()
def add_multiples(R, type=1, R0=0):
    """
    This function adds multiples to a synthetic reflectivity signal.
    
    Inputs:
    R     : Reflectivity; it is supposed to be sampled at time intervals given by
            dt=2*thick_i/v_i, i.e., the layer thicknesses are not constant.
    type  : 1 -> displacement wave; 0 -> pressure wave [optional, default=1].
    R0    : Surface reflectivity [optional, default=0].
    
    Output:
    RM    : Reflectivity with multiples, dimension of R.
    """
    
    # Check if the input is a column vector; otherwise, transpose it
    N, j = R.shape if len(R.shape) > 1 else (len(R), 1)
    if j > N:
        R = R.T  
        N = j
        transposed = True 
    else:
        transposed = False
    
    # Define "sign" based on the type of wave (displacement or pressure)
    sign = 1 if type == 1 else -1
    
    # Initialize U and D matrices for recursive calculations
    U = np.zeros((N + 1, N + 1))
    D = np.zeros((N + 1, N + 1))
    
    # Set the first down-propagating coefficient to 1
    D[0, 0] = 1
    
    GREY = "\033[90m"
    RESET = "\033[0m"
    
    bar_format = f"{GREY}{{l_bar}}{{bar}}{{r_bar}}{RESET}"
    
    # Recursive relations following eq. 3.38/3.39
    for k in tqdm(range(N), desc="Processing...", bar_format=bar_format):
        for n in range(k, -1, -1):
            U[n, k] = (1 + R[n]) * U[n + 1, k] - sign * R[n] * D[n, k - n]
            D[n + 1, k - n] = (1 - R[n]) * D[n, k - n] + sign * R[n] * U[n + 1, k]
        D[0, k + 1] = R0 * U[0, k]

    
    # Transmission through the surface
    RM = -sign * (1 + R0) * U[0, :N]
    
    # Transpose the output if the input was a row vector
    if transposed:
        RM = RM.T
    
    return RM