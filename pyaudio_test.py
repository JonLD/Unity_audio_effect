# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 17:16:33 2022

@author: JonLD
"""
import wave
import pyaudio


CHUNK = 48000

wf = wave.open('Oneshot_test.wav')

print(wf)


p = pyaudio.PyAudio()
 
    
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)

print(data)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()