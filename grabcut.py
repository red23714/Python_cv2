import numpy as np
import cv2

img = cv2.imread('messi5.jpg')

mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1,65), np.float64)
fgdModel = np.zeros((1,65), np.float64)

rect = (50,50,450,290)
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

newmask = cv2.imread('newmask.png',0)

mask[newmask == 0] = 0
mask[newmask == 255] = 1

mask, bgdModel, fgdModel = cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)

mask = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')

img = img*mask[:,:,np.newaxis]

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

