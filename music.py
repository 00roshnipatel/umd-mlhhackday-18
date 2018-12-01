from scipy.io import wavfile
import pyaudio, wave
import os

is_playing = True

def play_music(f, data, stream, chunk):
    #play stream
    while is_playing and data:
        stream.write(data)
        data = f.readframes(chunk)
