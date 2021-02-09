import cv2
import numpy as np

img = cv2.imread('C:/Users/red/Documents/Python/lico/frame1.jpg')

b = [100, 100, 100]

width, height, _ = img.shape
g = 1
while True:
    if g == 1:
        lower_black = np.array([0, 0, 0], dtype="uint16")
        upper_black = np.array(b, dtype="uint16")
        black_mask = cv2.inRange(img, lower_black, upper_black)

        cv2.imshow('img', black_mask)

        k = cv2.waitKey(30) & 0xFF

        if k == ord('a'):
            b[0] += 5
            b[1] += 5
            b[2] += 5
            g = 0
        else:
            if k == ord('d'):
                b[0] -= 5
                b[1] -= 5
                b[2] -= 5
                g = 0

        if k == 27:
            cap.release()
            cv2.destroyAllWindows()
    else:
        for x in range(0, width, 5):
            for y in range(0, height, 5):
                if img[x, y][0] > b[1] and img[x, y][1] > b[1]:
                    print('yes')
        g = 1
