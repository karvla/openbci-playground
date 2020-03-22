from time import sleep
from serial import Serial
import threading
from synthesizer import Synth

class Heartbeat(threading.Thread):
    def __init__(self, dev, synth, baudrate=9600):
        super(Heartbeat, self).__init__()
        self.reader = Serial(dev, 9600)
        self.synth = synth
        self.data = []

    def run(self):
        while True:
            self.await_heartbeat()
            self.synth.play_heartbeat()

    def await_heartbeat(self):
        line = self.reader.readline()
        print(int(line))
        return True

if __name__ == '__main__':
    synth = Synth()
    hb = Heartbeat('/dev/cu.usbmodem1421',synth)
    hb.start()
