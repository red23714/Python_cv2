import cv2
import numpy as np

img = cv2.imread('C:/Users/red/Documents/Python/lico/frame1.jpg')

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
bottomLeftCornerOfText = (300, 230)
fontScale = 2
fontColor = (255, 255, 255)
lineType = 2

cv2.putText(img, 'Hello, world!',
            bottomLeftCornerOfText,
            font,
            fontScale,
            fontColor,
            lineType)

while True:
    cv2.imshow('img', img)

    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        cap.release()
        cv2.destroyAllWindows()
