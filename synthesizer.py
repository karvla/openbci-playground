import pyaudio
import numpy as np
from time import sleep
from functools import reduce
import sys


VOLUME = 0.5     # range [0.0, 1.0]
FS = 44100       # sampling rate, Hz, must be integer
DURATION = 1.0   # in seconds, may be float
BLUES_SCALE_RATIOS = np.array([1, 6/5, 4/3, 45/32, 3/2, 9/5, 2])


def harmonize(waves):
    """ Returns a signal consisting of a sum of sine waves. """
    signal = list(reduce(lambda x, y : x + y, waves))
    signal = np.array(signal)
    return signal.astype(np.float32)

def get_waves(freqs):
    " Returns a numpy array with containing waves with different frequencies. "
    t = np.arange(FS*DURATION) / FS
    sine = lambda f : np.sin(2 * np.pi * f * t)
    waves = list(map(sine, freqs))
    return np.array(waves)

def blues_freqs(start_freq):
    """ Returns a blues scale in the key corresponding to start_freq. """
    return BLUES_SCALE_RATIOS * start_freq
    

def playback():
    """ Reads waves and plays them. Quite limited atm... """
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=FS,
                    output=True)

    while True:
        freqs = blues_freqs(440.0)
        waves = get_waves(freqs)
        signal = harmonize(waves)

        stream.write(VOLUME * signal)
        sleep(DURATION)

    stream.stop_stream()
    stream.close()

    p.terminate()

if __name__ == "__main__":
    playback()