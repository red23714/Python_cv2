import serial
import time
import struct

arduino = serial.Serial('COM18', 115200, timeout=.1)
while True:
    string = input()
    arduino.write(string.encode())
    print(string)
    time.sleep(1)

