import numpy as np
from time import sleep, time
from reader import Reader
from frequency_selection import freq_peaks, map_peaks, periodogram, band_power
from synthesizer import Synth
from random import random
from pulsereader import Heartbeat
import click

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
        for u in reader.latest_data()[:2]:
            freqs, psd = periodogram(u, T)
            _, theta, _, _, _ = band_power(freqs, psd)

            peaks_power = freq_peaks(freqs, psd, n=14)
            peaks_power = [
                (peak, power)
                for peak, power in peaks_power
                if peak > 4.0 and abs(50 - peak) > 3
            ]
            if peaks_power:
                peaks, power = zip(*peaks_power)
                print("Theta power", theta)
                print("Selected frequecies", [round(peak) for peak in peaks])
                peaks = [peak * 8 + 200 for peak in peaks]
                power = [p * 1e6 for p in power]
                synth.play_freq(peaks, 0.15, theta**2)
        sleep(1/theta/5)


if __name__ == "__main__":
    main()
