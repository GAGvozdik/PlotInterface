import numpy as np

# Define the tntamp function to compute the amplitude spectrum
from .decorators import work_time

@work_time(func_name='tntamp')
def tntamp(fdom, f, m):
    """
    Computes the amplitude spectrum of the wavelet.
    Args:
        fdom: Dominant frequency.
        f: Frequency vector.
        m: Shape parameter.
    Returns:
        Amplitude spectrum.
    """
    return np.exp(-(f / fdom) ** m)