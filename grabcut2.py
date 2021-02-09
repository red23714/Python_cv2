#!/usr/bin/env python

import cv2
import numpy as np
import math
import struct
i = 0
def nothing(*args):
    pass

if __name__ == '__main__':
   
    cv2.namedWindow("result")
    cap = cv2.VideoCapture(0)

    cv2.namedWindow('color_filter')  # Main window
    cv2.namedWindow('Settings')
    cv2.createTrackbar('h1', 'Settings', 67, 255, nothing)
    cv2.createTrackbar('s1', 'Settings', 62, 255, nothing)
    cv2.createTrackbar('v1', 'Settings', 0, 255, nothing)
    cv2.createTrackbar('h2', 'Settings', 90, 255, nothing)
    cv2.createTrackbar('s2', 'Settings', 255, 255, nothing)
    cv2.createTrackbar('v2', 'Settings', 241, 255, nothing)
    cv2.createTrackbar('black', 'Settings', 0, 1, nothing)
    color_blue = (255, 0, 0)
    color_red = (0, 0, 128)

    while True:
        flag, img = cap.read()
        img = cv2.flip(img, 1)

        # mask = np.zeros(img.shape[:2], np.uint8)

        # bgdModel = np.zeros((1,65), np.float64)
        # fgdModel = np.zeros((1,65), np.float64)

        # rect = (50,50,450,290)
        # cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

        # mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        # img = img*mask2[:,:,np.newaxis]

        h1 = cv2.getTrackbarPos('h1', 'Settings')
        s1 = cv2.getTrackbarPos('s1', 'Settings')
        v1 = cv2.getTrackbarPos('v1', 'Settings')
        h2 = cv2.getTrackbarPos('h2', 'Settings')
        s2 = cv2.getTrackbarPos('s2', 'Settings')
        v2 = cv2.getTrackbarPos('v2', 'Settings')
        black=cv2.getTrackbarPos('black', 'Settings')
        hsv_min = np.array((h1, s1, v1), np.uint8)
        hsv_max = np.array((h2, s2, v2), np.uint8)

        try:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            thresh = cv2.inRange(hsv, hsv_min, hsv_max)
            contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            for cnt in contours0:
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                center = (int(rect[0][0]), int(rect[0][1]))
                area = int(rect[1][0] * rect[1][1])
                if area > 500:
                    cv2.drawContours(img, [box], 0, color_blue, 2)
                    cv2.circle(img, center, 5, color_red, 2)
                    print(box[0][0])
            if (black == 0):
                cv2.imshow('result', img)
            else:     
                cv2.imshow('result', thresh) 
        except:
            cap.release()
            raise
        ch = cv2.waitKey(5)
        if ch == 27:
            cv2.imwrite("test.png", img)
            break

    cap.release()
    cv2.destroyAllWindows()
