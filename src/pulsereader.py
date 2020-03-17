from time import sleep
from serial import Serial

ser = Serial('/dev/ttyUSB0', 9600) # Establish the connection on a specific port

# TODO: use pyserial-asyncio
async def await_heartbeat():
    ser.readline()

if __name__ == '__main__':
    while True:
        print(int(ser.readline()))
        sleep(0.05)
