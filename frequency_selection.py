import numpy as np


def freq_peaks(freqs, power, n=1):
    """ Return the top n peaks from the freqs and power. """
    power_dt = np.gradient(power, freqs)
    freq_power_dpdf = sorted(zip(freqs, power, power_dt), key=lambda x: abs(x[2]))

    peaks = [(f, p) for f, p, _ in freq_power_dpdf]
    return peaks[:n]


if __name__ == "__main__":
    freq = np.arange(0, 10, 0.1)
    power = np.sin(freq)
    max_pair = freq_peaks(freq, power, 3)
    print(max_pair)
