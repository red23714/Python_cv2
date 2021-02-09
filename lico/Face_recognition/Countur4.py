import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
screen_width = 640
screen_height = 480
olx = 0
oly = 0
naprav = 0
param = cap.set(3, screen_width)
param = cap.set(2, screen_height)


def nothing(*args):
    pass


def createPath(image):
    height, weight = image.shape[:2]
    return np.zeros((height, weight, 3), np.uint8)  # 3 - number of channels HSV, 4 - ARGB


oldX = 0
oldY = 0
x = 0
y = 0
old_tim = 0

ret, frame = cap.read()
path = createPath(frame)

cv2.namedWindow('color_filter')  # Main window
cv2.namedWindow('Settings')
cv2.createTrackbar('h1', 'Settings', 102, 255, nothing)
cv2.createTrackbar('s1', 'Settings', 109, 255, nothing)
cv2.createTrackbar('v1', 'Settings', 18, 255, nothing)
cv2.createTrackbar('h2', 'Settings', 113, 255, nothing)
cv2.createTrackbar('s2', 'Settings', 230, 255, nothing)
cv2.createTrackbar('v2', 'Settings', 119, 255, nothing)
cv2.createTrackbar('black', 'Settings', 0, 1, nothing)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   

    h1 = cv2.getTrackbarPos('h1', 'Settings')
    s1 = cv2.getTrackbarPos('s1', 'Settings')
    v1 = cv2.getTrackbarPos('v1', 'Settings')
    h2 = cv2.getTrackbarPos('h2', 'Settings')
    s2 = cv2.getTrackbarPos('s2', 'Settings')
    v2 = cv2.getTrackbarPos('v2', 'Settings')
    black=cv2.getTrackbarPos('black', 'Settings')

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)
    color_filter = cv2.inRange(hsv, h_min, h_max)

    contours, hierarchy = cv2.findContours(color_filter.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (255, 0, 0), 3, cv2.LINE_AA, hierarchy, 1)
    thresh = cv2.inRange(hsv, h_min, h_max)

    moments = cv2.moments(color_filter, 1)

    sumX = moments['m10']
    sumY = moments['m01']
    count = moments['m00']

    if count > 100:
        x = int(sumX / count)
        y = int(sumY / count)
        cv2.circle(color_filter, (x, y), 10, (0, 0, 255), 0)

    if oldX > 0 and oldY > 0:
        tim = int(time.perf_counter() * 10)
        if tim - old_tim >= 2:
            olx = x
            oly = y
            old_tim = tim

        vx = (x - olx) / 0.2
        vy = (y - oly) / 0.2
        if vx > 0 and vy > 0:
            naprav = 3
        elif vx < 0 and vy > 0:
            naprav = 4
        elif vx < 0 and vy < 0:
            naprav = 1
        elif vx > 0 and vy < 0:
            naprav = 2
        print(vy, vx, naprav)

        cv2.line(path, (oldX, oldY), (x, y), (0, 0, 255), 5)
    oldX = x
    oldY = y

    frame = cv2.add(frame, path)

    #cv2.imshow('color_filter', frame)

    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

    frame = cv2.flip(frame, 1)
    cv2.putText(frame, "%d, %d" % (x, y), (screen_width - (x + 10), y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    if (black == 0):
        cv2.imshow('color_filter', frame)
    else:    
        thresh = cv2.flip(thresh, 1) 
        cv2.imshow('color_filter', thresh) 

cap.release()
cv2.destroyAllWindows()
