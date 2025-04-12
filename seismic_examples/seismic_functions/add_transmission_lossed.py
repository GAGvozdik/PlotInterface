import numpy as np
from .decorators import work_time
from tqdm import tqdm

@work_time()
def add_transmission_lossed (R, R0 = 0):
    # this function add multiples to a synthetic reflectivity signal and,
    # possibly, the trasmission coefficient of the surface
    # Inputs
    #  R     Reflectivity; it is supposed to be sampled at time intervals given by
    #        dt=2*thick_i/v_i, i.e. the layer thicknesses are not constant
    #  R0    surface reflectivity [optional, default=0]
    #  Output
    #  RTL   Reflectivity with transmission losses, dimension of R
    # 

    # %let's define the default value for R0 when it is not passed
    # When you did not define R0, it will set as 0
    N,J = R.shape if len(R.shape) > 1 else (len(R), 1)
    if J > N:
        R = R.T
        N = J
        transpose = True
    else:
        transpose = False

    # initialize the reflection coefficients
    RTL = np.copy(R)  # question 
    
    GREY = "\033[90m"
    RESET = "\033[0m"
    
    bar_format = f"{GREY}{{l_bar}}{{bar}}{{r_bar}}{RESET}"
    
    for n in tqdm(range(N), desc="Processing...", bar_format=bar_format):
        for j in range(n):    
            RTL[n] = RTL[n]*(1-R[j]**2)

    RTL = (1+R0)*RTL

    if transpose == True:
        RTL = RTL.T
    return RTL
