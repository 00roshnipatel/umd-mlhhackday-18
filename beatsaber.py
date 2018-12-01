import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()

    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(frame, contours, -1, (0,255,0), 3)

    cv2.imshow('frame', img)
    
    c = cv2.waitKey(1)
    if c == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

