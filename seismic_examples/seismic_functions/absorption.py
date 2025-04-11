import numpy as np
from .decorators import work_time

@work_time(func_name='absorption')
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
    
    # Compute the attenuation factor recursively
    for i in range(1, N):
        a[i] = a[i - 1] * np.exp(-dt * fdom * np.pi / q[i - 1])
    
    # Apply attenuation to the reflectivity signal
    ra = r * a
    
    # Transpose the output if the input was a row vector
    if transpose:
        ra = ra.T
    
    return ra