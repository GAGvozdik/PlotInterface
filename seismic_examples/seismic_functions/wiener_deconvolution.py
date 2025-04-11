import numpy as np


# 1. Frequency Domain Wiener Deconvolution
from .decorators import work_time

@work_time(func_name='wiener_deconvolution')
def wiener_deconvolution(input_signal, wavelet, noise_level=0.01):
    n = len(input_signal) + len(wavelet) - 1
    input_signal_padded = np.pad(input_signal, (0, n - len(input_signal)))
    wavelet_padded = np.pad(wavelet, (0, n - len(wavelet)))
    
    H = np.fft.fft(wavelet_padded)
    G = np.fft.fft(input_signal_padded)
    H_conj = np.conj(H)
    wiener_filter = H_conj / (H * H_conj + noise_level**2)
    
    R_est = np.fft.ifft(G * wiener_filter)
    return np.real(R_est[:len(input_signal)])
