import pyaudio
import wave
import threading
from threading import Thread, Lock
from time import sleep, time


class Audio_player(threading.Thread):
    def __init__(self, path):
        super(Audio_player, self).__init__()
        self.mutex = Lock()
        self.chunk = 1024
        self.path = path
        self.feed = wave.open(path, "rb")
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.audio.get_format_from_width(self.feed.getsampwidth()),
            channels=self.feed.getnchannels(),
            rate=int(self.feed.getframerate() / 2),
            output=True,
        )
        self.rate = 1.0
    
    def run(self):
        data = self.feed.readframes(self.chunk)
        rate = self.rate
        while data:
            if self.rate != rate:
                rate = self.rate
                self.set_rate(rate)
            self.stream.write(data)
            data = self.feed.readframes(self.chunk)

    def set_rate(self, rate=1.0):
        self.stream.close()
        self.stream = self.audio.open(
            format=self.audio.get_format_from_width(self.feed.getsampwidth()),
            channels=self.feed.getnchannels(),
            rate=int(rate * self.feed.getframerate()),
            output=True,
        )


if __name__ == "__main__":
    ap = Audio_player("./Jon Hopkins - Open Eye Signal (Original Mix).wav")
    init_rate = 0.5
    ap.set_rate(init_rate)
    ap.start()
    for i in range(2000):
        sleep(0.5)
        ap.rate = init_rate + 0.1
