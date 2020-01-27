import pyaudio
import numpy as np

from time import sleep
from functools import reduce
from frequency_selection import freq_peaks


class Synth:

    def __init__(self):
        self.duration = 0.1
        self.sf = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.sf,
                        output=True)

    def harmonize(self,waves):
        """ Returns a signal consisting of a sum of sine waves. """
        signal = list(reduce(lambda x, y : x + y, waves))
        signal = np.array(signal)
        return signal.astype(np.float32)

    def sound_waves(self, freqs):
        " Returns a numpy array with containing waves with different frequencies. "
        t = np.arange(self.sf*self.duration) / self.sf
        sine = lambda f : np.sin(2 * np.pi * f * t)
        waves = list(map(sine, freqs))
        return np.array(waves)

    def blues_freqs(self, start_freq):
        """ Returns a blues scale in the key corresponding to start_freq. """
        blues_scale_ratio = np.array([1, 6/5, 4/3, 45/32, 3/2, 9/5, 2])
        return blues_scale_ratio * start_freq
        
    def play_signal(self, volume, signal):
        self.stream.write(volume * signal)

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        
if __name__ == "__main__":
    playback()