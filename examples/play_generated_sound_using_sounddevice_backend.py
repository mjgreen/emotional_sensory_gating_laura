#!/home/matt/anaconda3/bin/python3.7

import numpy as np
import sounddevice as sd

# sample rate
sd.default.samplerate = 44100
# duration
time = 0.04
# frequency
frequency = 1000
# Generate time of samples between 0 and two seconds
samples = np.arange(44100 * time) / 44100.0
# Recall that a sinusoidal wave of frequency f has formula w(t) = A*sin(2*pi*f*t)
wave = 10000 * np.sin(2 * np.pi * frequency * samples)
# Convert it to wav format (16 bits)
wav_wave = np.array(wave, dtype=np.int16)
# we use blocking when in a script to prevent too-early exit
sd.play(wav_wave, blocking=True)
