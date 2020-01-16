from time import sleep, time
import numpy as np
from reader import Reader
from plotter import Plotter
from scipy import signal
from scipy.integrate import simps

VOLTS_PER_COUNT = (4500000)/24/(2**23-1)
#VOLTS_PER_COUNT = 1.2 * 8388607.0 * 1.5 * 51.0
sf = 200
h = 1/sf
t_len = 500
t = np.arange(t_len)/h

def periodogram(u, t):
    """ Returns the power spectral density for different
        frequencies using welch method. """
    win = 4*sf
    freqs, psd = signal.welch(u, sf, nperseg=win)
    return freqs, psd

def pad(u, n=256):
    zeros = np.zeros(256)
    return np.concatenate((zeros, u, zeros), axis=0)

def realative_power(a, b, freqs, psd):
    """
    Computes the relative power of the signal between a hz and b hz.
    """
    dx = freqs[1] = freqs[0]
    index = np.logical_and(freqs >= a, freqs <=b)
    ab_power = simps(psd[index], dx=dx)
    total_power = simps(psd, dx=dx)
    return ab_power / total_power
    


def main():
    r = Reader('C4:A9:D2:20:3F:A1')
    r.start()
    plot = Plotter()
    
    while len(r.channels[0]) < t_len:
        sleep(0.1)

    while True:
        for n in range(4):
            u = r.channels[n][-t_len:]
            freqs, psd = welch_method(u, t)
            plot.add(freqs, psd, n)

            print(realative_power(4, 8, freqs, psd), " ", end='')
        print()
        plot.update_plot()
        sleep(0.001)

if __name__ == "__main__":
    main()
