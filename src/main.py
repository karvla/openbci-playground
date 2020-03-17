import numpy as np
from time import sleep, time
from reader import Reader
from frequency_selection import freq_peaks, map_peaks, periodogram
from synthesizer import Synth
from random import random
from pulsereader import await_heartbeat
import click
import asyncio

SF = 200
T_LEN = 1000
 

@click.command()
@click.option('--interface', default='udp', help='data interface, bt or udp')
@click.option('--mac', default="", help='bluetooth mac-address of the EEG')
def main(interface, mac):
    synth = Synth()
    r = Reader(mac=mac.lower(), interface=interface)
    r.start()
    t = np.arange(T_LEN) / SF

    print("Waiting for data")
    while len(r.channels[0]) < T_LEN:
        sleep(0.1)

    synth.start()
    f = 880
    
    async def play():
        while True:
            u = r.channels[0][-T_LEN:]
            freqs, psd = periodogram(u, t)
            peaks, _ = zip(*freq_peaks(freqs, psd, n=7))
            peaks = map_peaks(peaks)
            await asyncio.wait_for(await_heartbeat(), timeout=1.0)
            synth.play_heartbeat()
            synth.play_freq(peaks[0:2], random(), random()*0.5)
            #sleep(1.0)
            #synth.play_freq(peaks[3:4], random(), random()*0.2)
            #sleep(1.0)
            #synth.play_freq(peaks[2:3], random(), random()*0.2)
            #sleep(1.0)
            #synth.play_freq(peaks[2:3], random(), random()*0.2)
            #sleep(1.0)

            #synth.play_freq(peaks[0:1], 2.0)
            #sleep(1.0)
            #synth.play_freq(peaks[1:3], 0.5)
            #sleep(1.0)
            #synth.play_freq(peaks[2:4], 0.5)
            #sleep(1.0)
            #synth.play_freq(peaks[4:5], 0.5)
            #sleep(1.0)
    asyncio.run(play())

        # waves = synth.sound_waves(peaks)
        # signal = synth.harmonize(waves)
        # synth.play_signal(volume=0.5, signal=signal)
        # sleep(synth.duration)

if __name__ == "__main__":
    main()

