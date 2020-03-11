Transanimus
==================

Transanimus is an art projects that lets you listen to someones brainwaves. Connects to an OpenBCI Ganglion board either directly through bluetooth (not supported on Windows) or via a UDP stream from OpenBCI GUI. Python 3.4, 3.5, or 3.6 is required for Windows users. Any Python 3 should work on Linux or macOS.

## Usage

Install the dependencies using `pipenv install`. 

* Connect via UDP by launching OpenBCI GUI and start a UDP stream of a time series using the Newworking widget. Then run `python src/main.py --interface udp` 

* Connect via Bluetooth by running `python3 src/main.py --interface bt --mac <macadress>`, where \<macadress\> is the bluetooth mac adress of the Ganglion Board. Lookup the mac adress using `sudo hcitool -i hci0 lescan`.
 
