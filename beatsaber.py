import cv2
import numpy as np
import time
import pyaudio, wave
import os
import threading

from game import *
import music

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

# set up screen
SCREEN_WIDTH = int(cap.get(3))
SCREEN_HEIGHT = int(cap.get(4))

game_manager = GameManager((SCREEN_WIDTH, SCREEN_HEIGHT))
renderer = Renderer(game_manager)

curr_time = time.time()

# === Music ===
#define stream chunk
chunk = 2048

#open a wav format music
fname = "assets/bubbles_long.wav"
f = wave.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fname),"rb")
#instantiate PyAudio
p = pyaudio.PyAudio()
#open stream
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                channels = f.getnchannels(),
                rate = f.getframerate(),
                output = True)
#read data
data = f.readframes(chunk)

music_t = threading.Thread(target=music.play_music, args=(f,data,stream,chunk)).start()

while cap.isOpened():
    # read in from webcam and do contours
    ret, frame = cap.read()
    thresh = fgbg.apply(frame)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # update time
    delta_time = time.time() - curr_time
    curr_time = time.time()

    # test output
    pts = flatten_contour(cull_noise(contours))
    game_manager.update(pts, delta_time)
    render = renderer.render()
    cv2.imshow('Bubbles', cv2.cvtColor(cv2.flip(render, 1), cv2.COLOR_BGR2RGB))

    # exit keys
    c = cv2.waitKey(1)
    if c == ord('q'):
        break

music.is_playing = False

#stop stream
stream.stop_stream()
stream.close()

#close PyAudio
p.terminate()

cap.release()
cv2.destroyAllWindows()
