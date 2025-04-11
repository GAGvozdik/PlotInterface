import numpy as np

# Define the mwindow function to create a tapering window
from .decorators import work_time

@work_time(func_name='mwindow')
def mwindow(nsamps, percent):
    """
    Creates a tapering window.
    Args:
        nsamps: Number of samples.
        percent: Percentage of the signal to taper.
    Returns:
        Tapering window.
    """
    m = int(nsamps * percent / 100)
    w = np.hanning(2 * m + 1)
    window = np.ones(nsamps)
    window[:m] = w[:m]
    window[-m:] = w[-m:]
    return window