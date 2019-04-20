#!/usr/bin/env python3

import pyaudio
pa = pyaudio.PyAudio()
i = pa.open(rate=44100, format=pyaudio.paFloat32, channels=2, input=True)  # opens a recording (an input device)
print('starting to record from mic')
d = i.read(41000 * 10)  # actually makes the recording
o = pa.open(rate=44100, format=pyaudio.paFloat32, channels=2, output=True)  # opens an output device (a playback device)
print('starting to playback what I just recorded')
o.write(d)  # write means play I think
print('ok')
