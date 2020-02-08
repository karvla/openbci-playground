from time import sleep, time
import numpy as np
from reader import Reader
from plotter import Plotter
from scipy import signal
from scipy.integrate import simps

sf = 200
t_len = 1000
t = np.arange(t_len) / sf


def periodogram(u, t, n_win=4):
    """ Returns the power spectral density for different
        frequencies using welch method. """
    win = int(t_len / n_win)
    freqs, power = signal.welch(u, sf, nperseg=win)
    return freqs, power


def pad(u, n=256):
    zeros = np.zeros(256)
    return np.concatenate((zeros, u, zeros), axis=0)


def relative_power(a, b, freqs, psd):
    """
    Computes the relative power of the signal between a hz and b hz.
    """
    dx = freqs[1] - freqs[0]

    index = np.logical_and(freqs >= a, freqs <= b)
    index_50_hz = np.logical_and(freqs >= 45, freqs <= 55)

    ab_power = simps(psd[index], dx=dx)
    total_power = simps(psd, dx=dx) - simps(psd[index_50_hz], dx=dx)
    return round(ab_power / total_power, 3)

def band_power(freqs, psd):
    delta = relative_power(0.5, 3, freqs, psd)
    theta = relative_power(3, 8, freqs, psd)
    alpha = relative_power(8, 12, freqs, psd)
    beta = relative_power(12, 38, freqs, psd)
    gamma = relative_power(38, 42, freqs, psd)
    return delta, theta, alpha, beta, gamma


def heartrate(u, t):
    freqs, psd = periodogram(u, t, 2)
    index_max = np.argmax(psd)
    return freqs[index_max]


def main():
    r = Reader(mac="e0:06:15:36:28:44", interface="udp")
    r.start()
    plot = Plotter()
    [
        plot.set_properties(n, x_label="f", y_label="V^2/Hz", x_lim=(0, 50))
        for n in range(4)
    ]

    while len(r.channels[0]) < t_len:
        sleep(0.1)

    while True:
        for n in range(4):
            u = r.channels[n][-t_len:]
            freqs, psd = periodogram(u, t)
            plot.add(freqs, psd, n)
            # plot.add(t, u, n)

            rel_power = round(
                relative_power(4, 8, freqs, psd), 3
            )  # Power in theta range.
            print(rel_power, " ", end="")
            if n == 0:
                print(heartrate(u, t), end="")
        print()
        plot.update_plot()
        sleep(0.2)


if __name__ == "__main__":
    main()
