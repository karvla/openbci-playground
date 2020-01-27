import numpy as np


def freq_peaks(freqs, power, n=1):
    """ Return the top n peaks from the freqs and power. """
    power_dt = np.gradient(power, freqs)
    peaks = list(filter(lambda x: abs(x[2]) < 0.05, zip(freqs, power, power_dt)))
    peaks_by_power = sorted(peaks, key=lambda x: abs(x[1]), reverse=True)

    peaks = [(f, p) for f, p, _ in peaks_by_power[:n]]
    return peaks


if __name__ == "__main__":
    freq = np.arange(0, 10, 0.1)
    power = np.sin(freq)
    max_pair = freq_peaks(freq, power, 3)
    print(max_pair)
