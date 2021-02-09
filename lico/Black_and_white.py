import cv2
import numpy as np

cap = cv2.VideoCapture(0)
screen_width = 520
screen_height = 740
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

ret, frame = cap.read()
path = createPath(frame)

cv2.namedWindow('color_filter')  # Main window
cv2.namedWindow('Settings')
cv2.createTrackbar('h1', 'Settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'Settings', 74, 255, nothing)
cv2.createTrackbar('v1', 'Settings', 88, 255, nothing)
cv2.createTrackbar('h2', 'Settings', 93, 255, nothing)
cv2.createTrackbar('s2', 'Settings', 132, 255, nothing)
cv2.createTrackbar('v2', 'Settings', 241, 255, nothing)

while True:
    ret, frame = cap.read()
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

    if oldX > 0 and oldY > 0:
        cv2.line(path, (oldX, oldY), (x, y), (0, 0, 255), 5)
    oldX = x
    oldY = y
    cv2.putText(frame, "%d, %d" % (x, y), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    frame = cv2.add(frame, path)

    cv2.imshow('color_filter', frame)

    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
