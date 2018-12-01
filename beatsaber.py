import cv2
import numpy as np

cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=25, detectShadows=True)

while cap.isOpened():
    ret, frame = cap.read()

    thresh = fgbg.apply(frame)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(frame, contours, -1, (0,255,0), 3)

    cv2.imshow('frame', cv2.flip(img, 1))
    
    c = cv2.waitKey(1)
    if c == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

