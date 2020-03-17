import pyaudio
import numpy as np
from time import sleep, time
from functools import reduce
from frequency_selection import freq_peaks
from threading import Thread
import scipy.io.wavfile
from scipy import signal as scisig
from pathlib import Path

samples = Path(__file__).parent.parent / "samples/"

class Synth(Thread):

    def __init__(self):
        super(Synth, self).__init__()
        self.count = 0
        self.has_changed = False
        self.duration = 100
        self.sf = 44100
        self.atack = -10.0
        self.res = 4
        self.window_idx = 0
        self.frame_count = 4096
        self.freq = 440.0
        self.wave = self._sound_wave(440.0) / 10000
        self.mod_freq = False
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.res),
                        channels=1,
                        rate=self.sf,
                        output=True,
                        stream_callback=self._callback,
                        frames_per_buffer=self.frame_count)


    def _callback(self, in_data, frame_count, time_info, status):
        data = self.wave[frame_count * self.window_idx : frame_count * (self.window_idx + 1)]
        self.window_idx += 1

        # Rolling back the track every 100 frames
        lim = 100
        if self.window_idx == lim:
            self.window_idx = 0
            self.wave = np.roll(self.wave, -lim*frame_count)

        return (data.tobytes(), pyaudio.paContinue)

    def play_freq(self, freqs, duration, amplitude=0.1):
        t0 = time() 
        signals = self._sound_waves(freqs, duration)
        signal = self.harmonize(signals)
        signal = self.fade(signal)
        signal = self.convolve(signal)
        signal = self.fade(signal)
        signal = self.set_amplitude(signal, amplitude)
        self._add_to_track(signal)

    def play_sample(self, sample, amplitude=0.1):
        t0 = time() 
        _, sample = scipy.io.wavfile.read(sample)
        sample = self.set_amplitude(sample, amplitude)
        self._add_to_track(sample)

    def play_heartbeat(self, amplitude=0.6):
        heart_beat_fn = Path(__file__).parent.parent / "samples/heartbeat-single.wav"
        self.play_sample(heart_beat_fn)

    def _add_to_track(self, signal):
        frame_end = self.window_idx*(self.frame_count+1)
        signal_end = frame_end + signal.shape[0]
        self.wave[frame_end:signal_end] += signal

    def fade(self, signal):
        fade_len = int(signal.shape[0]*0.1)
        t1 = np.arange(-fade_len/2, fade_len/2) / ((fade_len)/2)
        a1 = 1 / (1 + np.exp(-10 * t1))
        a2 = 1 / (1 + np.exp(10 * t1))

        t2 = np.arange(-signal.shape[0]/2, signal.shape[0]/2) / ((signal.shape[0])/2)
        
        signal[:fade_len] = a1 * signal[:fade_len]

        signal[-fade_len:] = a2 * signal[-fade_len:]

        return signal

    def convolve(self, signal):
        _, impulse_response = scipy.io.wavfile.read(samples / "1st_baptist_nashville_balcony.wav")
        impulse_response = impulse_response[:,0]
        signal = scisig.convolve(signal, impulse_response, method='fft')

        return signal

    def set_amplitude(self, signal, amplitude):
        return signal/np.max(np.abs(signal))*amplitude


    def modulate(self, freq):
        self.mod_freq = True
        self.freq = freq

    def run(self):
        self.stream.start_stream()
        while self.stream.is_active():
            sleep(0.1)

    def _sound_wave(self, freq, duration=None):
        if not duration:
            duration = self.duration
        t = np.arange(self.sf * duration) / self.sf
        wave = np.sin(2 * np.pi * freq * t)
        return wave.astype(np.float32)


    def _sound_waves(self, freqs, duration=None):
        " Returns a numpy array with containing waves with different frequencies. "
        amplitude = 0.1
        if not duration:
            duration = self.duration
        t = np.arange(self.sf * duration) / self.sf
        sine = lambda f : np.sin(2 * np.pi * f * t)*amplitude
        waves = list(map(sine, freqs))
        return np.array(waves)

    def harmonize(self, waves):
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
