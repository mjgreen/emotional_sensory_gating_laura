#!/home/matt/anaconda3/bin/python3.7

import os
import datetime
import random
import shutil
import sys
import subprocess
import time
import pandas as pd
import numpy as np
import io
from pyo import Sine, createServerGUI, Server
from contextlib import redirect_stdout

with redirect_stdout(io.StringIO()):
    from psychopy import logging, prefs
logging.console.setLevel(logging.WARNING)
prefs.hardware['audioLib'] = ["pyo"]
from psychopy import sound, core
sound_info = 'Using %s for sound backend in psychopy' % sound.audioLib


# Server().boot().start().gui()


def return_sounds():

    beep_file = sound.Sound('sounds/lijffijt_40ms_90dB_1000Hz_4ms_rise_fall.wav')

    sample_rate = 44100
    duration = 0.04
    frequency = 1000
    samples = np.arange(sample_rate * duration) / float(sample_rate)  # Generate time of samples between 0 and two seconds
    # Recall that a sinusoidal wave of frequency f has formula w(t) = A*sin(2*pi*f*t)
    wav = 10000 * np.sin(2 * np.pi * frequency * samples)
    # Convert it to wav format (16 bits)
    wav_wave = np.array(wav, dtype=np.int16)
    beep_wave = sound.Sound(value=wav_wave, secs=0.04, loops=1, volume=0.0001)

    beep_sine = Sine(freq=1000).play()

    return beep_file, beep_wave, beep_sine


def sound_trial():
    sleep = 0.04

    time.sleep(.5)

    file.play()
    time.sleep(sleep)
    time.sleep(.5)

    wave.play()
    time.sleep(sleep)
    time.sleep(.5)

    sine.out(dur=.04)
    time.sleep(sleep)
    time.sleep(.5)

    # time.sleep(.5)


num_trials = 5
trial_order = ['beep' for n in range(num_trials)]

print(sound_info)
print('trial order is %s' % trial_order)

# print("starting jack server")
# subprocess.check_output("jack_control start", shell=True)
# print("jack server {}".format(subprocess.check_output("jack_control status", shell=True).decode("utf-8").replace("\n", " ")))

file, wave, sine = return_sounds()
start_time = time.time()
print("session start time in ms since epoch: {:.1f}".format(time.time()))

n_beeps_per_trial = 3.0
est_trial_dur = 2000.0
nmsinasec=1000.0

for trial in range(len(trial_order)):
    trial_type = trial_order.pop(0)
    trial_start_time = time.time()
    sound_trial()
    trial_end_time = time.time()
    trial_dur = trial_end_time - trial_start_time
    trial_dur_in_ms = trial_dur * nmsinasec
    mean_beep_dur = (trial_dur_in_ms-est_trial_dur) / n_beeps_per_trial
    overhead = trial_dur_in_ms - (est_trial_dur + (40.0 * n_beeps_per_trial))
    print("total trial time = {:.2f} ms, idealised trial time is {:.2f} ms, trial overhead = {:.1f} ms, % trial overhead = {:.4f} %\t mean beep duration ~~ {:.2f} ms, ideal beep duration is {:.2f} ms, so {:.2f} ms is mean beep overhead".format(
        trial_dur_in_ms,
        est_trial_dur + (40.0 * n_beeps_per_trial),
        overhead,
        overhead/trial_dur_in_ms,
        mean_beep_dur,
        40.00,
        overhead/n_beeps_per_trial))
    #
    # print("mean beep duration on trial {:02d} of {:02d} start time in ms since session start time: {:.10f}".format(trial + 1, num_trials, (time.time() - start_time)))
    # sound_trial()
    # time.sleep(1)

print('\nthe end\n')
