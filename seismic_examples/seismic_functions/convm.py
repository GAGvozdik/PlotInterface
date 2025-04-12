import numpy as np
from scipy.signal import convolve
import warnings
from .mwhalf import mwhalf
from .decorators import work_time
from tqdm import tqdm

@work_time()
def convm(r, w, pct=10):
    """
    CONVM: convolution followed by truncation for min phase filters
    
    Parameters:
    r ... reflectivity (1D array or 2D array where columns are traces)
    w ... wavelet (1D array)
    pct ... percent taper at the end of the trace to reduce truncation effects (default=10)
    
    Returns:
    s ... convolved output with same dimensions as input r
    
    This is a Python adaptation of the MATLAB 'convm' function for seismic convolution.
    It performs convolution while maintaining the input length and applying a taper.
    """
    
    # Convert inputs to numpy arrays if they aren't already
    r = np.array(r)
    w = np.array(w).flatten()  # Ensure wavelet is 1D
    
    # Store original dimensions
    orig_shape = r.shape
    if r.ndim == 1:
        r = r.reshape(-1, 1)  # Convert to column vector if 1D
    
    nsamps, ntr = r.shape  # Get number of samples and traces
    
    # Apply warning if wavelet is longer than input (commented out as in original)
    # if len(w) > nsamps:
    #     warnings.warn('second argument longer than the first, output truncated to length of first argument.')
    
    # Initialize output array
    s = np.zeros_like(r)
    
    # Create taper window
    if pct > 0:
        mw = mwhalf(nsamps, pct)  # Apply cosine taper
    else:
        mw = np.ones(nsamps)  # No taper
    
    GREY = "\033[90m"
    RESET = "\033[0m"
    bar_format = f"{GREY}{{l_bar}}{{bar}}{{r_bar}}{RESET}"
    
    # Perform convolution for each trace
    for k in tqdm(range(ntr), desc="Processing...", bar_format=bar_format):
        temp = convolve(r[:, k], w, mode='full')  # Full convolution
        s[:, k] = temp[:nsamps] * mw  # Truncate to input length and apply taper
    
    # Restore original dimensions
    if len(orig_shape) == 1:
        s = s.flatten()  # Return to 1D if input was 1D
    
    return s
