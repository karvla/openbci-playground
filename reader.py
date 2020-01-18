import threading
from time import sleep, time
import socket
import json


class Reader(threading.Thread):
    def __init__(self, **kwargs):
        super(Reader, self).__init__()
        self.channels = [[], [], [], []]
        self.mac = kwargs.get('mac', None)
        self.interface = kwargs.get('interface', 'bt')


    def run(self):
        if self.interface == 'bt':
            from pyOpenBCI import OpenBCIGanglion
            print("Connecting to bluetooth...")
            self.board = OpenBCIGanglion(mac=self.mac)
            print("Connected!")
            self.board.start_stream(self._read_bt)
        elif self.interface == 'udp':
            UDP_IP = "127.0.0.1"
            UDP_PORT = 12345
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((UDP_IP, UDP_PORT))
            self._read_udp(sock)

    def _values_to_volts(self, values):
        VOLTS_PER_COUNT = 1.2 * 8388607.0 * 1.5 * 51.0
        return [values[n] / VOLTS_PER_COUNT for n in range(4)]

    def _read_udp(self, socket):
            while True:
                data, addr = socket.recvfrom(1024) # buffer size is 1024 bytes
                data_dict = json.loads(data)
                volts = self._values_to_volts(data_dict['data'])
                self._add_samples(volts)


    def _read_bt(self, sample):
        volts = self._values_to_volt(sample.channels_data)
        self._add_samples(volts)


    def _add_samples(self, samples):
        [self.channels[i].append(samples[i]) for i in range(4)]


