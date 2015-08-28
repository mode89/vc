import numpy as np

def dct(y):
    N = len(y)
    y2 = np.empty(2 * N, float)
    y2[:N] = y[:]
    y2[N:] = y[::-1]
    c = np.fft.rfft(y2)
    phi = np.exp(-1j * np.pi * np.arange(N) / (2 * N))
    return np.real(phi * c[:N])
