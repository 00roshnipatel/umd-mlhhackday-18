from scipy.io import wavfile
import pyaudio, wave
import os

def play_music(f, data, stream, chunk):
    #play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)
