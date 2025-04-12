import numpy as np
from .decorators import work_time
from tqdm import tqdm

@work_time()
def mwhalf(n, pct):
    """
    Create a cosine taper window (helper function for convm)
    
    Parameters:
    n ... length of the window
    pct ... percentage of the end to taper
    
    Returns:
    window ... taper window array
    """
    m = int(np.round(n * pct / 100))  # Number of samples to taper
    if m == 0:
        return np.ones(n)
    
    # Create cosine taper for the last m samples
    window = np.ones(n)
    taper = (1 + np.cos(np.linspace(0, np.pi, m))) / 2
    window[-m:] = taper
    
    return window