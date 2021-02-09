import serial
import time
import struct

arduino = serial.Serial('COM18', 115200, timeout=.1)
while True:
    strang = 'pythön!'
    arduino.write(strang.encode())
    time.sleep(1)

