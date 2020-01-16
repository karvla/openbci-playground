import threading
from pyOpenBCI import OpenBCIGanglion
from time import sleep, time

VOLTS_PER_COUNT = 1.2 * 8388607.0 * 1.5 * 51.0

class Reader(threading.Thread):
    def __init__(self, mac):
        super(Reader, self).__init__()
        self.channels = [[], [], [], []]
        print("Connecting...")
        self.board = OpenBCIGanglion(mac=mac)
        print("Connected!")

    def run(self):
        self.board.start_stream(self.read)

    def read(self, sample):
        volts = sample.channels_data * VOLTS_PER_COUNT
        [self.channels[i].append(volts[i]) for i in range(4)]


