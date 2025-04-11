import numpy as np
from .decorators import work_time

@work_time(func_name='gain')
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
    g = np.zeros_like(t)
    for i in range(len(t)):
        g[i] = (t[i] / (2 * V)) ** 2
    return g
    