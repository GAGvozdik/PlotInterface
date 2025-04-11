import numpy as np
from .decorators import work_time

@work_time(func_name='reflec_from_model')
def reflec_from_model(rho, v, q, thk, dt, tmax=None):
    """
    This function generates a reflectivity signal from a multilayer model,
    defined in terms of its velocity, density, and thicknesses.
    
    Inputs:
    rho    : density, dimension nlayers
    v      : velocity, dimension nlayers
    q      : quality factor, dimension nlayers 
    thk    : thicknesses, dimension nlayers-1
    dt     : sampling interval 
    tmax   : total modelled time, optional; when missing, the total time is
             twice the last reflection time
    
    Outputs:
    R      : Reflectivity
    V      : Velocity, same dimension as R
    RHO    : Density, same dimension as R
    Q      : Quality factor, same dimension as R
    DTHK   : Double-valued Thicknesses, same dimension as R
    T      : Time, same dimension as R
    """

    NLayers = len(rho)  # Number of layers
    t = np.zeros(NLayers)  # Initialize time array
    
    # Calculate the two-way travel time for each layer
    for i in range(NLayers - 1):   # question?
        t[i] = 2 * thk[i] / v[i]
    
    # Calculate the total time for the last layer
    if tmax is not None:
        t[-1] = max(2 * np.sum(t[:-1]), tmax)  # question [:-1]
    else:
        t[-1] = 2 * np.sum(t[:-1])
    
    # Round times to the nearest multiple of dt
    t = np.floor(t / dt) * dt
    
    # Calculate the number of subdivisions per layer
    n = (t / dt).astype(int) # ensure not a decimal
    
    
    # Total number of subdivisions
    N = np.sum(n)
    
    # Initialize output arrays
    R = np.zeros(N)
    V = np.zeros(N)
    RHO = np.zeros(N)
    Q = np.zeros(N)
    DTHK = np.zeros(N)
    T = np.zeros(N)
    
    k = 0  # Counter for the output arrays
    
    # Populate the output arrays
    for i in range(NLayers):
        for j in range(n[i]):
            V[k] = v[i]
            RHO[k] = rho[i]
            Q[k] = q[i]
            DTHK[k] = 2 * dt * v[i]
            T[k] = (k + 1) * dt
            if j == 0 and i != 0:  # Calculate reflectivity at the interface
                i1 = rho[i - 1] * v[i - 1]
                i2 = rho[i] * v[i]
                R[k] = (i2 - i1) / (i1 + i2)
            k += 1
    
    return R, V, RHO, Q, DTHK, T