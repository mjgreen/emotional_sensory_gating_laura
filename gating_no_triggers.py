#!/home/matt/anaconda3/bin/python3.7
# -*- coding: utf-8 -*-
"""
This is the version without triggers.
In development it is being done in linux with anaconda3 python 3.7
The no_triggers version is intended to be run on win7 in psychopy3 in P103
The triggers version is intended to be run in win7 on P213's Z440
"""

from pyo import Server, Sine  # SfPlayer # SfPlayer is for sound files; Sine is ok if we are generating our own sound from pyo itself
import time
import random
import os
import platform
from psychopy import visual, event, core, monitors, parallel, gui

def get_parallel_port_address():
    if platform.system() == 'Linux':
        try:
            parallel_port = parallel.ParallelPort(address='/dev/parport0')
            print(parallel_port)
        except OSError:
            print("Parallel port cock-up: No such device or address: '/dev/parport0': " +
                  "Did you run 'sudo rmmod lp ; sudo modprobe ppdev' yet?: " +
                  "Did you do 'sudo adduser matt lp' to get access to the port?\n")
            core.quit()
        else:
            there_is_a_parallel_port = True
            return there_is_a_parallel_port, parallel_port
    elif platform.system() == 'Windows':
        try:
            parallel_port = parallel.ParallelPort(address=0x1FF8)  # eeg z440
            # psychopy.logging.flush()
        except RuntimeError:
            print("Parallel port cock-up:\n")
            # "On Windows, 64bit Python can't use inpout32's parallel port driver, which cocks everything up.\n" +
            # "The solution is to use 32 bit python instead. Build psychopy using pip from the 32 bit python.\n" +
            # "Make sure inpout32.dll is in the toplevel at runtime.\n")
            there_is_a_parallel_port = False
            parallel_port = None
            return there_is_a_parallel_port, parallel_port
        else:
            there_is_a_parallel_port = True
            return there_is_a_parallel_port, parallel_port


def make_window():
    viewpixx = monitors.Monitor("eeg", width=54, distance=53)
    viewpixx.setSizePix((1920, 1080))
    viewpixx.saveMon()
    monitor = viewpixx
    which_screen = 1
    print("using {} monitor".format(monitor.name))
    xpx = monitor.getSizePix()[0]
    ypx = monitor.getSizePix()[1]
    xcm = monitor.getWidth()
    # win = visual.Window(fullscr=True, size=[xpx, ypx], units='pix', allowGUI=False, waitBlanking=True, color=[0, 0, 0], monitor=monitor.name, screen=which_screen, winType=None)
    win = visual.Window(fullscr=False, size=[800, 600], units='pix', allowGUI=True, waitBlanking=True, color=[0, 0, 0], monitor=monitor.name, screen=which_screen, winType=None)
    actual_frame_rate = win.getActualFrameRate()
    print("actual frame rate: {} Hz".format(int(round(actual_frame_rate))))
    return win

def press_any_key_when_ready(win):
    txt = visual.TextStim(win, "Press any key when you are ready to continue")
    txt.draw()
    win.flip()
    event.waitKeys()
    win.flip()

def take_a_break(win):
    txt = visual.TextStim(win, "Please take a break.")
    txt.draw()
    win.flip()
    event.waitKeys()
    win.flip()

def do_fix_cross(win):
    extent = 10
    fixation = visual.ShapeStim(win, vertices=((0, -extent), (0, extent), (0, 0), (-extent, 0), (extent, 0)), lineWidth=2, closeShape=False, lineColor="black")
    fixation.draw()
    win.flip()

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

def graceful_exit(s, win):
    s.stop()
    win.close()
    core.quit()

def get_participant_number():
    my_dlg = gui.Dlg(title="gating")
    my_dlg.addField('Participant number:')
    ok_data = my_dlg.show()  # show dialog and wait for OK or Cancel
    if my_dlg.OK:  # or if ok_data is not None
        print(ok_data)
    else:
        print('user cancelled')
    participant_number = ok_data[0]
    return participant_number

def run():
    participant_number = get_participant_number()
    os.path.isdir("results") or os.mkdir("results")
    results_directory = os.path.join("results", str(participant_number).zfill(3))
    os.path.isdir(results_directory) or os.mkdir(results_directory)
    results_file = str(participant_number).zfill(3) + "_results.dlm.csv"
    results_path = os.path.join(results_directory, results_file)
    trial_info_header = "participant\tblock\ttrl\tprebeep\tbeep1\tinterbeep\tbeep2\tpostbeeps\r\n"
    with open(results_path, "a") as f:
        f.write(trial_info_header)
    # parallel_port = get_parallel_port_address()
    win = make_window()
    s = start_sound_server()
    beep = construct_sound(beep_hz=1000.0)
    number_of_trials = 160
    break_trials = [39, 79, 119]
    silence_before_beeps = 2.000
    beep_duration = 0.010  # Laura = 0.010 as of 23 May (was previously 0.040)
    silence_between_beeps = 0.500
    fixed_duration = silence_before_beeps + beep_duration + silence_between_beeps + beep_duration
    min_duration = 6.0  # min_duration_total - fixed_duration # Laura = 6 seconds
    max_duration = 8.0  # max_duration_total - fixed_duration # Laura = 8 seconds
    block_number = 1
    press_any_key_when_ready(win)
    for t in range(number_of_trials):

        do_fix_cross(win)

        # parallel_port.setData(0)

        time.sleep(silence_before_beeps)

        beep_number = 1
        trigger_code = (beep_number*10) + block_number
        beep1on = time.time()
        # parallel_port.setData(trigger_code)
        beep.out(dur=beep_duration)
        time.sleep(beep_duration)
        beep1off = time.time()

        time.sleep(silence_between_beeps)

        beep_number = 2
        trigger_code = (beep_number * 10) + block_number
        beep2on = time.time()
        # parallel_port.setData(trigger_code)
        beep.out(dur=beep_duration)
        time.sleep(beep_duration)
        beep2off = time.time()

        post_beep_silence_dur = random.uniform(min_duration, max_duration)
        t0 = core.getTime()
        while core.getTime() - t0 < post_beep_silence_dur:
            k = event.getKeys(keyList=['escape'])
            if k:
                print("quitting because experimenter pressed escape")
                win.close()
                core.quit()

        trial_info = "{}\t{}\t{:3s}\t{}\t{:.12f}\t{}\t{:.12f}\t{}\r\n".format(participant_number, block_number, str(t+1).zfill(3), 1000.0*silence_before_beeps, 1000.0*(beep1off-beep1on), 1000.0*silence_between_beeps, 1000.0*(beep2off-beep2on), 1000.0*post_beep_silence_dur)

        with open(results_path, "a") as f:
            f.write(trial_info)

        print(trial_info)

        if t in break_trials:
            take_a_break(win)
            block_number += 1

    # number_of_trials has been reached
    s.stop()
    win.close()
    core.quit()
