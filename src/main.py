import numpy as np

from time import sleep, time
from reader import Reader
from frequency_selection import freq_peaks, map_peaks, periodogram
from synthesizer import Synth
import random

SF = 200
T_LEN = 1000


def main():
    synth = Synth()
    r = Reader(mac="C4:A9:D2:20:3F:A1".lower(), interface="udp")
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
        peaks, _ = zip(*freq_peaks(freqs, psd, n=7))
        peaks = map_peaks(peaks)
        synth.play_freq(peaks[0:1], 2.0)
        sleep(1.0)
        synth.play_freq(peaks[1:3])
        sleep(1.0)
        synth.play_freq(peaks[2:4])
        sleep(1.0)
        synth.play_freq(peaks[4:5])
        sleep(1.0)


        # waves = synth.sound_waves(peaks)
        # signal = synth.harmonize(waves)
        # synth.play_signal(volume=0.5, signal=signal)
        # sleep(synth.duration)



if __name__ == "__main__":
    main()
