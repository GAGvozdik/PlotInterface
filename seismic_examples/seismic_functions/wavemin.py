# Define the wavemin function to generate a minimum-phase wavelet
from scipy.fftpack import fft, ifft  # For Fourier transforms
import numpy as np
from .tntamp import tntamp
from .levrec import levrec
from .decorators import work_time
from tqdm import tqdm

@work_time()
def wavemin(dt, fdom, tlength, m=7, stab=0.000001):
    """
    Generates a minimum-phase wavelet.
    Args:
        dt: Sampling interval.
        fdom: Dominant frequency.
        tlength: Total duration of the wavelet.
        m: Shape parameter (default is 4).
        stab: Stabilization factor (default is 0.000001).
    Returns:
        w: The wavelet.
        tw: Time vector.
    """
    # Check if m is within the valid range
    if m < 2 or m > 7:
        raise ValueError('m must lie between 2 and 7')
    
    # Adjust the dominant frequency based on the value of m
    m_dict = {
        2: (-0.0731, 1.0735),
        3: (0.0163, 0.9083),
        4: (0.0408, 0.8470),
        5: (-0.0382, 0.8282),
        6: (0.0243, 0.8206),
        7: (0.0243, 0.8206)
    }
    f0, m0 = m_dict[m]
    fdom2 = (fdom - f0) / m0
    
    # Create the time vector
    nt = int(2 * tlength / dt) + 1
    nt = 2 ** int(np.ceil(np.log2(nt)))  # Round up to the next power of 2
    tmax = dt * (nt - 1)
    tw = np.arange(0, tmax + dt, dt)
    
    # Create the frequency vector
    fnyq = 1.0 / (2 * (tw[1] - tw[0]))  # Nyquist frequency
    f = np.linspace(0, fnyq, nt // 2 + 1)
    
    # Create the power spectrum
    tmp = tntamp(fdom2, f, m)
    powspec = tmp ** 2
    
    # Create the autocorrelation
    auto = np.real(ifft(powspec))
    auto[0] *= (1 + stab)
    
    # Run the Levinson algorithm to compute the wavelet
    nlags = int(tlength / dt) + 1
    b = np.zeros(nlags)
    b[0] = 1.0
    winv = levrec(auto[:nlags], b)
    
    # Invert winv to get the wavelet
    w = np.real(ifft(1.0 / fft(winv)))
    tw = dt * np.arange(len(w))
    
    # Normalize the wavelet
    w = w / np.max(np.abs(w))
    return w, tw