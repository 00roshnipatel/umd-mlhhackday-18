import cv2
import numpy as np
import time

from game import *

def cull_noise(points):
    """Tries to get rid of noise"""
    new_list = []
    for p in points:
        if len(p) > 1:
            new_list.append(p)
    return new_list

def flatten_contour(l):
    points = []
    for data in l:
        for p in data:
            points.append(( p[0][0],p[0][1] ))
    return points

cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=25, detectShadows=True)

game_manager = GameManager()
renderer = Renderer(game_manager)

curr_time = time.time()

while cap.isOpened():
    # read in from webcam and do contours
    ret, frame = cap.read()
    thresh = fgbg.apply(frame)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #img = cv2.drawContours(frame, cull_noise(contours), -1, (255, 255,255), 3)

    # update time
    delta_time = time.time() - curr_time
    curr_time = time.time()

    # test output
    pts = flatten_contour(cull_noise(contours))
    game_manager.update(pts, delta_time)
    render = renderer.render()
    cv2.imshow('frame', cv2.flip(render, 1))

    # exit keys
    c = cv2.waitKey(1)
    if c == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
