import serial
import time
# arduino = serial.Serial('COM18', 9600, timeout=.1)
# time.sleep(1)

def write(x1):
	while True:
		 if(x1 > 0):
		     arduino.write(serial.to_bytes([255, 0, 0, 0])) #Left motor - max, Right motor - 0, Left = 1, Right = 1
		     time.sleep(5)
		print(x1)
	    # arduino.write(serial.to_bytes([0, 0, 1, 1]))   #Left motor - release, Right motor - release
	    # time.sleep(1)

	    # arduino.write(serial.to_bytes([0, 255, 0, 0])) #Left motor - 0, Right motor - max
	    # time.sleep(5)


