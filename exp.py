#!/home/matt/anaconda3/bin/python3.7
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:49:34 2019

@author: matt
"""

from pyo import SfPlayer, Server, Sine
import time
import os
import io
import socket
import random
from contextlib import redirect_stdout
with redirect_stdout(io.StringIO()):
    from psychopy import visual


def start():
    global s
    global num_trials
    global n_beeps_per_trial
    global est_trial_dur
    global n_ms_in_one_second
    global tone_dur
    global win
    os.chdir('/home/matt/PycharmProjects/emotional_sensory_gating_laura/')
    s = Server(sr=48000, nchnls=2, buffersize=2048, duplex=0, audio='jack', jackname='pyo')
    s.setOutputDevice(0)
    s.deactivateMidi()
    s.boot()
    s.start()
    num_trials = 160
    n_beeps_per_trial = 2.0
    est_trial_dur = 2.000 + 0.040  + 0.5000 + 0.040
    n_ms_in_one_second = 1000.0
    tone_dur = 0.04
    hostname = socket.gethostname()
    if hostname == 'dingo':
        win = visual.Window(monitor="monitor_e330", units='pix', winType='pyglet', size=(400, 400), pos=(1920-300, 0), allowGUI=True, screen=0, fullscr=False)
    else:
        win = visual.Window(monitor="monitor_eeg", units='pix', winType='pyglet', allowGUI=False, screen=1, fullscr=True)
    extent = 10
    fixation = visual.ShapeStim(win, vertices=((0, -extent), (0, extent), (0, 0), (-extent, 0), (extent, 0)), lineWidth=2, closeShape=False, lineColor="black")
    fixation.draw()
    win.flip()


def return_sounds():
    beep_file = SfPlayer('sounds/lijffijt_40ms_90dB_1000Hz_4ms_rise_fall.wav').play()
    beep_sine = Sine(freq=[1000, 1000])
    return beep_file, beep_sine


def run():
    start()
    file, sine = return_sounds()
    for trial in range(num_trials):
        trial_start_time = time.time()

        time.sleep(2.000)
        # trigger 1
        file.out()                                 # or sine.out(dur=tone_dur)
        time.sleep(0.040)
        time.sleep(0.500)
        # trigger 2
        file.out()                                 # or sine.out(dur=tone_dur)
        time.sleep(0.040)
        time.sleep(random.random(.550, .750))

        trial_end_time = time.time()
        trial_dur = trial_end_time - trial_start_time
        trial_dur_in_ms = trial_dur * n_ms_in_one_second
        mean_beep_dur = (trial_dur_in_ms - est_trial_dur) / n_beeps_per_trial
        overhead = trial_dur_in_ms - est_trial_dur

        print("trial {}: total trial time = {:.2f} ms, ideal trial time is {:.2f} ms, trial overhead = {:.1f} ms, or {:.4f} %, mean beep duration ~~ {:.2f} ms, ideal beep duration is {:.2f} ms, so {:.2f} ms is mean beep overhead".format(str(trial+1).zfill(3), trial_dur_in_ms, est_trial_dur, overhead, overhead/trial_dur_in_ms, mean_beep_dur, n_ms_in_one_second * tone_dur, overhead/n_beeps_per_trial))

        if trial+1 in [40, 80, 120]:
            print("take a break")
            input("press a key when ready to proceed")

    s.stop()
    win.close()

