import pyaudio
import numpy as np

from time import sleep
from functools import reduce
from frequency_selection import freq_peaks

from threading import Thread

class Synth(Thread):

    def __init__(self):
        super(Synth, self).__init__()
        self.count = 0
        self.has_changed = False
        self.duration = 100
        self.sf = 44100
        self.fade_len = 10
        self.atack = -10.0
        self.res = 4
        self.window_idx = 0
        self.frame_count = 4096
        self.freq = 440.0
        self.wave = self._sound_wave(440.0)
        self.mod_freq = False
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.res),
                        channels=1,
                        rate=self.sf,
                        output=True,
                        stream_callback=self._callback,
                        frames_per_buffer=self.frame_count)


    def _callback(self, in_data, frame_count, time_info, status):
        # if self.mod_freq:
        #     data = self.wave[frame_count * self.window_idx : frame_count * (self.window_idx + 1)]
        #     data[self.zero_local_idx:] = 0
            
        #     import sys
        #     np.set_printoptions(threshold=sys.maxsize)
        #     print(data)

        #     self._sound_wave(self.freq)
        #     self.window_idx = 0
        #     self.mod_freq = False
        # else:
        #     data = self.wave[frame_count * self.window_idx : frame_count * (self.window_idx + 1)]
        #     self.window_idx += 1

        # next_data = self.wave[frame_count * self.window_idx : frame_count * (self.window_idx + 1)]
        # self.zero_local_idx = np.where(np.abs(next_data)  < 0.01)[0][0]
        # # print(self.zero_local_idx)

        data = self.wave[frame_count * self.window_idx : frame_count * (self.window_idx + 1)]
        print(np.min(data), np.max(data))
        self.window_idx += 1
        
        return (data.tobytes(), pyaudio.paContinue)


    def fade(self, signal):
        t1 = np.arange(-self.fade_len/2, self.fade_len/2) / ((self.fade_len)/2)
        a1 = 1 / (1 + np.exp(-1 * t1))
        a2 = 1 / (1 + np.exp(1 * t1))

        t2 = np.arange(-signal.shape[0]/2, signal.shape[0]/2) / ((signal.shape[0])/2)
        signal = np.sin(2 * np.pi * 2 * t2)

        signal[:self.fade_len] = a1 * signal[:self.fade_len]

        signal[-self.fade_len:] = a2 * signal[-self.fade_len:]

        return signal


    def _sound_wave(self, freq):
        t = np.arange(self.sf * self.duration) / self.sf
        wave = np.sin(2 * np.pi * freq * t)
        wave = self.fade(wave)

        return wave.astype(np.float32)

    def modulate(self, freq):
        self.mod_freq = True
        self.freq = freq


    def run(self):
        self.stream.start_stream()
        while self.stream.is_active():
            sleep(0.1)

    def sound_waves(self, freqs):
        " Returns a numpy array with containing waves with different frequencies. "
        t = np.arange(self.sf * self.duration) / self.sf
        sine = lambda f : np.sin(2 * np.pi * f * t)
        waves = list(map(sine, freqs))
        return np.array(waves)

    def harmonize(self,waves):
        """ Returns a signal consisting of a sum of sine waves. """
        signal = list(reduce(lambda x, y : x + y, waves))
        signal = np.array(signal)
        return signal.astype(np.float32)

    def blues_freqs(self, start_freq):
        """ Returns a blues scale in the key corresponding to start_freq. """
        blues_scale_ratio = np.array([1, 6/5, 4/3, 45/32, 3/2, 9/5, 2])
        return blues_scale_ratio * start_freq
        
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        
if __name__ == "__main__":
    playback()