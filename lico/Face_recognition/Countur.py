import cv2
import numpy as np
import time
import serial
import struct

from threading import Thread

arduino = serial.Serial('COM18', 9600, timeout=.1)

cap = cv2.VideoCapture(0)
screen_width = 320
screen_height = 240
param = cap.set(3, screen_width)
param = cap.set(2, screen_height)

x1 = 0
y1 = 0

doit = True
oldTime = 0
def doit():
	global x1
	global y1
	global newTime
	global oldTime
	while doit:
		newTime = time.time() * 1000
		if(newTime - oldTime > 1000):
			x2 = x1
			if(x2 > 0):
				arduino.write(serial.to_bytes([255, 255, 0, 1])) #Left motor - max, Right motor - 0, Left = 1, Right = 1
				time.sleep(abs(x2 * 1.0) / 100)
			else: 
				if(x1 < 0):
					arduino.write(serial.to_bytes([255, 255, 1, 0])) #Left motor - max, Right motor - 0, Left = 1, Right = 1
					time.sleep(abs(x2 * 1.0) / 100)
			time.sleep(0.01)
			oldTime = newTime
			print(x1)
my_thread = Thread(target = doit)
my_thread.start()


def nothing(*args):
    pass


oldX = 0
oldY = 0
x = 0
y = 0

ret, frame = cap.read()

cv2.namedWindow('color_filter')  # Main window
cv2.namedWindow('Settings')
cv2.createTrackbar('h1', 'Settings', 67, 255, nothing)
cv2.createTrackbar('s1', 'Settings', 62, 255, nothing)
cv2.createTrackbar('v1', 'Settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'Settings', 90, 255, nothing)
cv2.createTrackbar('s2', 'Settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'Settings', 241, 255, nothing)

oldTime = time.time() * 1000

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h1 = cv2.getTrackbarPos('h1', 'Settings')
    s1 = cv2.getTrackbarPos('s1', 'Settings')
    v1 = cv2.getTrackbarPos('v1', 'Settings')
    h2 = cv2.getTrackbarPos('h2', 'Settings')
    s2 = cv2.getTrackbarPos('s2', 'Settings')
    v2 = cv2.getTrackbarPos('v2', 'Settings')

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)
    color_filter = cv2.inRange(hsv, h_min, h_max)

    contours, hierarchy = cv2.findContours(color_filter.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (255, 0, 0), 3, cv2.LINE_AA, hierarchy, 1)

    moments = cv2.moments(color_filter, 1)

    sumX = moments['m10']
    sumY = moments['m01']
    count = moments['m00']

    if count > 100:
        x = int(sumX / count)
        y = int(sumY / count)
        cv2.circle(color_filter, (x, y), 10, (0, 0, 255), 0)

    width = screen_width / 2
    height = screen_height / 2
    if x != width or y != height:
        x1 = x - width
        y1 = y - height


    cv2.putText(frame, "%d, %d" % (x, y), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow('color_filter', frame)

    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        doit = False
        break

cap.release()
cv2.destroyAllWindows()
