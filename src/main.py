import numpy as np
from time import sleep, time
from reader import Reader
from frequency_selection import freq_peaks, map_peaks, periodogram
from synthesizer import Synth
from random import random
from pulsereader import Heartbeat
import click
import asyncio

SF = 200
T_LEN = 1000
T = np.arange(T_LEN) / SF


@click.command()
@click.option("--interface", default="udp", help="data interface, bt or udp")
@click.option("--mac", default="", help="bluetooth mac-address of the EEG")
@click.option("--pulsedev", default="", help="device for reading pulse")
def main(interface, mac, pulsedev):
    synth = Synth()
    reader = Reader(mac=mac.lower(), interface=interface)
    reader.start()
    synth.start()

    if pulsedev:
        heartbeat = Heartbeat(dev=pulsedev, synth=synth)
        heartbeat.start()

    while reader.waiting_for_data():
        sleep(0.1)

    while True:
        u = reader.latest_data()[0]
        freqs, psd = periodogram(u, T)
        peaks, _ = zip(*freq_peaks(freqs, psd, n=7))
        peaks = map_peaks(peaks)
        synth.play_freq([peaks[0]], 0.15, random() * 0.5)
        sleep(1.0)


if __name__ == "__main__":
    main()
