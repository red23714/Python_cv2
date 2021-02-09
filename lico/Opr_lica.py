import cv2

cap = cv2.VideoCapture(0)
n = 1
while True:
#    ret, frame = cap.read()
    img = cv2.imread('C:/Users/red/Documents/Python/lico/frame1.jpg')
    cv2.imshow('frame',img)

    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
#    if(n == 1):
#       cv2.imwrite("frame1.jpg",  frame)
#      n = 0

cap.release()
cv2.destroyAllWindows()
