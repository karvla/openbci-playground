# from openbci import ganglion as bci
# print(dir(bci))

from time import sleep, time
from threading import Thread
import numpy as np
import matplotlib.pyplot as plt
import reader


VOLTS_PER_COUNT = 1.2 * 8388607.0 * 1.5 * 51.0
SAMPLE_POINTS = 200

# TODO: Move to class

def plot(x, y):
    if len(x) > SAMPLE_POINTS:
        plt.axis([0, 100, -0.01, 0.01])
        padding = [0] * 32
        s = np.array(padding + x + padding)
        s = s[-SAMPLE_POINTS:]
        sp = np.fft.fft(s, axis=0)
        timestep = y[-1] - y[-2]   # should be ~200Hz
        print(timestep)
        freq = np.fft.fftfreq(s.shape[0], timestep)
        i = freq > 0  # get positive half of frequencies
        plt.plot(freq[i], sp.real[i])
        #plt.pause(0.01)
        plt.cla()  # clear axes


def main():
    r = reader.Reader('C4:A9:D2:20:3F:A1')
    r.start()
    task = loop.create_task(r.get_samples)

    while True:
        x = r.samples
        y = r.timings
        plot(x, y)


if __name__ == "__main__":
    main()
