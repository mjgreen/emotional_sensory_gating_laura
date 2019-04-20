#!/home/matt/anaconda3/bin/python3.7
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:49:34 2019

@author: matt
"""

from pyo import Server, Sine  # SfPlayer
from itertools import chain
import time
import csv
# import os
import io
import socket
import random
from contextlib import redirect_stdout
with redirect_stdout(io.StringIO()):
    from psychopy import visual

def make_window():
    hostname = socket.gethostname()
    if hostname == 'dingo':
        win = visual.Window(monitor="monitor_e330", units='pix', winType='pyglet', size=(400, 400), pos=(1920 - 400, 0), allowGUI=True, screen=0, fullscr=False)
    elif hostname == 'matt-Lenovo-ideapad-100S-14IBR':
        win = visual.Window(monitor="monitor_e330", units='pix', winType='pyglet', size=(400, 400), pos=(1366 - 400, 0), allowGUI=True, screen=0, fullscr=False)
    else:
        win = visual.Window(monitor="monitor_eeg", units='pix', winType='pyglet', allowGUI=False, screen=1, fullscr=True)
    extent = 10
    fixation = visual.ShapeStim(win, vertices=((0, -extent), (0, extent), (0, 0), (-extent, 0), (extent, 0)), lineWidth=2, closeShape=False, lineColor="black")
    fixation.draw()
    win.flip()
    return win

def start_sound_server():
    s = Server(sr=48000, nchnls=2, buffersize=2048, duplex=0, audio='jack', jackname='pyo')
    s.setOutputDevice(0)
    s.deactivateMidi()
    s.boot()
    s.start()
    return s

def construct_sound(beep_hz=1000.0):
    beep = Sine(freq=[beep_hz, beep_hz]).play()
    return beep

def run():
    try:
        # print("\n")  # just to start console output with a blank line
        with open("beep_times.dlm", "w+") as f:
            f.write("trl  beep_1_duration  beep_2_duration\r\n")
        win                       =  make_window()
        print("  matt: Starting the sound server up now: warnings will be suppressed...")
        with redirect_stdout(io.StringIO()):
            s                     =  start_sound_server()
        beep                      =  construct_sound(beep_hz=1000.0)
        number_of_trials          =  160
        break_trials              =  [39, 79, 119]
        silence_before_beeps      =    2.000
        beep_duration             =    0.040
        silence_between_beeps     =    0.500
        fixed_duration            =  silence_before_beeps + beep_duration + silence_between_beeps + beep_duration
        min_duration_total        =    8.000
        max_duration_total        =   10.000
        min_duration              =  1  # min_duration_total - fixed_duration
        max_duration              =  2  # max_duration_total - fixed_duration
        beep1times = []
        beep2times = []
        print("  matt: About to run {} trials now...".format(number_of_trials))
        for t in range(number_of_trials):

            # CORE TRIAL SEQUENCE

            time.sleep(silence_before_beeps)

            beep1on = time.time()
            beep.out(dur=beep_duration)
            time.sleep(beep_duration)
            beep1off = time.time()

            time.sleep(silence_between_beeps)

            beep2on = time.time()
            beep.out(dur=beep_duration)
            time.sleep(beep_duration)
            beep2off = time.time()

            post_beep_silence_dur = random.uniform(min_duration, max_duration)
            time.sleep(post_beep_silence_dur)

            # POST- TRIAL SEQUENCE

            beep1dur = 1000.0 * (beep1off - beep1on)
            beep2dur = 1000.0 * (beep2off - beep2on)

            beep1times.append(beep1dur)
            beep2times.append(beep2dur)

            with open("beep_times.dlm", "a") as f:
                f.write("{:3s}  {:.12f}  {:.12f}\r\n".format(str(t+1).zfill(3), beep1dur, beep2dur))

            print("  matt: trial {:3s}: pre-beeps = {}; beep 1 = {:.1f}; inter-beeps = {}; beep 2 = {:.1f}, post-beeps = {:.1f}".format(str(t+1).zfill(3), int(1000.0*silence_before_beeps), beep1dur, int(1000.0*silence_between_beeps), beep2dur, 1000.0*post_beep_silence_dur))

            if t in break_trials:
                input('\ttake a break: the experimenter will resume the experiment soon: >>')
    except:
        print("\n  matt : Something went wrong, or user quit deliberately\n")
        s.stop()
        win.close()
    s.stop()
    win.close()
# TODO send beep durations to matplotlib for a histogram
