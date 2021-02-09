#!/usr/bin/env python

import cv2
import numpy as np
import math
import struct
i = 0
n = 1
m = 0
middle_x = 0
middle_y = 0
x = 0
y = 0
raspberrypi = False;
def nothing(*args):
    pass

if __name__ == '__main__':
   
    cv2.namedWindow("result")
    cap = cv2.VideoCapture(1)

    cv2.namedWindow('Picture')
    cv2.namedWindow('Settings')
    cv2.createTrackbar('h1', 'Settings', 67, 255, nothing) #67
    cv2.createTrackbar('s1', 'Settings', 62, 255, nothing) #62
    cv2.createTrackbar('v1', 'Settings', 0, 255, nothing) #0
    cv2.createTrackbar('h2', 'Settings', 90, 255, nothing) #90
    cv2.createTrackbar('s2', 'Settings', 255, 255, nothing) #255
    cv2.createTrackbar('v2', 'Settings', 241, 255, nothing) #241
    cv2.createTrackbar('black', 'Settings', 0, 1, nothing) 
    color_blue = (255, 0, 0)
    color_red = (0, 0, 128)

    while True:
        flag, img = cap.read()
        img = cv2.flip(img, 1)

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

                edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
                edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

                # usedEdge = edge1
                # if cv2.norm(edge2) > cv2.norm(edge1):
                #     usedEdge = edge2

                # reference = (1, 0)  # horizontal edge
                # angle = 180.0 / math.pi * math.acos(
                #  (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv2.norm(reference) * cv2.norm(usedEdge)))
                angle = ' '
                list_storon = []
                if area > 5000:
                    middle_x += rect[0][0]
                    middle_y += rect[0][1]
                    m += 1
                    n = 0
                    cv2.drawContours(img, [box], 0, color_blue, 2)
                    cv2.circle(img, center, 5, color_red, 2)
                    cv2.putText(img, str(area), (center[0]+20, center[1]-20),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, color_red, 2)
                    if(m == 5):
                        middle_y = middle_y / m
                        middle_x = middle_x / m
                        y = middle_y
                        x = middle_x
                        middle_x = 0
                        m = 0


                    if(raspberrypi == False):
                        if (black == 0 and len(contours0) > 0):
                            try:
                                w = rect[1][0] #1, 0
                                h = rect[1][1] #1, 1
                                crop_img = img[int(y - 200):int(y + 200), int(x - w/2):int(x + w/2)]
                                print("################")
                                print(x, rect[0][1])
                                print(y, rect[0][0])
                                print("################")
                                if(len(crop_img) > 0 and n == 0): #and center1 == (y - x)
                                    cv2.imwrite("res.png", crop_img)
                                    print("Yes")
                                    cv2.imshow('Picture', crop_img)
                                    n = 1
                            except cv2.error:
                                print("Error")
                            cv2.imshow('result', img)
                        else:     
                            cv2.imshow('result', thresh) 
        except:
            cap.release()
            raise
        ch = cv2.waitKey(5)
        if ch == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
