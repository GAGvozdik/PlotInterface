import numpy as np  # Import the NumPy library for numerical operations
from .decorators import work_time

@work_time(func_name='add_geometric_spreading')
def add_geometric_spreading(R, THK):
    # This function adds geometric spreading attenuation to a synthetic reflectivity signal
    # Inputs:
    # R     : Reflectivity (1D numpy array)
    # THK   : Layer thicknesses (1D numpy array)
    # Output:
    # RGS   : Reflectivity with geometric spreading (1D numpy array)

    RGS = np.zeros_like(R)  # Initialize an array of zeros with the same shape as R
    N = len(R)  # Get the number of elements in the reflectivity array

    for i in range(N):  # Loop through each element in the reflectivity array
        RGS[i] = (THK[0] / np.sum(THK[:i+1])) * R[i]  # Apply geometric spreading formula

    return RGS  # Return the reflectivity with geometric spreading