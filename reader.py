import threading
from pyOpenBCI import OpenBCIGanglion
from time import sleep, time
import asyncio

VOLTS_PER_COUNT = 1.2 * 8388607.0 * 1.5 * 51.0
SAMPLE_POINTS = 200

class Reader(threading.Thread):
    def __init__(self, mac):
        super(Reader, self).__init__()
        self.timings = []
        self.samples = []
        print("Connecting...")
        self.board = OpenBCIGanglion(mac=mac)
        print("Connected!")
        self.last_time = time()

    def run(self):
        self.board.start_stream(self.read)

    async def get_samples(self):
        await asyncio.sleep(0.005)

        return self.samples, self.timings

    def read(self, sample):
        volts = sample.channels_data / VOLTS_PER_COUNT
        self.timings.append(time())
        self.samples.append(volts[1])
        

