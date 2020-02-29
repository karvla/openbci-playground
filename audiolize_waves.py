import numpy as np

from time import sleep, time
from reader import Reader
from main import periodogram
from frequency_selection import freq_peaks
from synthesizer import Synth
import random

SF = 200
T_LEN = 1000


def map_peaks(peaks):
    """ Maps peaks to be in an audible range """
    return [20 + 10*peak for peak in peaks]

def audiolize():

    synth = Synth()
    r = Reader(mac="e0:06:15:36:28:44", interface="udp")
    r.start()
    t = np.arange(T_LEN) / SF

    print("Waiting for data")
    while len(r.channels[0]) < T_LEN:
        sleep(0.1)

    synth.start()
    f = 880
    while True:
        u = r.channels[0][-T_LEN:]
        freqs, psd = periodogram(u, t)
        peaks, _ = zip(*freq_peaks(freqs, psd, n=3))
        peaks = map_peaks(peaks)
        sleep(5*random.random())
        synth.play_freq(peaks)


        # waves = synth.sound_waves(peaks)
        # signal = synth.harmonize(waves)
        # synth.play_signal(volume=0.5, signal=signal)
        # sleep(synth.duration)



if __name__ == "__main__":
    audiolize()
