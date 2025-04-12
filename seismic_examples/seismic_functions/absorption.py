import numpy as np
from .decorators import work_time
from tqdm import tqdm

@work_time()
def absorption(r, q, dt, fdom):
    """
    This function adds attenuation losses to a synthetic reflectivity signal.
    
    Inputs:
    r     : Reflectivity (numpy array).
    q     : Quality factor (same dimension as r).
    dt    : Sampling interval (scalar).
    fdom  : Dominant frequency (scalar).
    
    Output:
    ra    : Reflectivity with attenuation (no frequency dependence).
    """
    # Check if the input is a column vector; otherwise, transpose it
    N, j = r.shape if len(r.shape) > 1 else (len(r), 1)
    if j > N:
        R = R.T
        N = j
        transpose = True
    else:
        transpose = False
        # Initialize the attenuation factor array
    a = np.ones_like(r)
    
    GREY = "\033[90m"
    RESET = "\033[0m"
    bar_format = f"{GREY}{{l_bar}}{{bar}}{{r_bar}}{RESET}"
    
    # Compute the attenuation factor recursively
    for i in tqdm(range(1, N), desc="Processing...", bar_format=bar_format):
        a[i] = a[i - 1] * np.exp(-dt * fdom * np.pi / q[i - 1])
    
    # Apply attenuation to the reflectivity signal
    ra = r * a
    
    # Transpose the output if the input was a row vector
    if transpose:
        ra = ra.T
    
    return ra