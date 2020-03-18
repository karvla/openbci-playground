from time import sleep
from serial import Serial
import threading

class Heartbeat(threading.Thread):
    def __init__(self, dev, synth, baudrate=9600):
        super(Heartbeat, self).__init__()
        self.reader = Serial(dev, 9600)
        self.synth = synth

    def run(self):
        while True:
            self.await_heartbeat()
            self.synth.play_heartbeat()

    def await_heartbeat(self):
        self.reader.readline()
        return True

if __name__ == '__main__':
    while True:
        print(int(ser.readline()))
        sleep(0.05)
