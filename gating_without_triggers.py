import time
import random
import os
import platform
from psychopy import visual, event
from psychopy import logging, prefs, monitors, gui, parallel
logging.console.setLevel(logging.DEBUG)
prefs.hardware['audioLib'] = ['pygame']
from psychopy import sound, core
print('Using %s for sounds' % sound.audioLib)

#parallel_port = parallel.ParallelPort(address=0x1FF8)  # eeg z440

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
    win = visual.Window(fullscr=True, size=[xpx, ypx], units='pix', allowGUI=False, waitBlanking=True, color=[0, 0, 0], monitor=monitor.name, screen=which_screen, winType=None)
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
    fixation = visual.ShapeStim(win, vertices=((0, -extent), (0, extent), (0, 0), (-extent, 0), (extent, 0)), lineWidth=2, closeShape=False, lineColor="black", autoLog=False)
    fixation.draw()
    win.flip()

def start_sound_server():
    if platform.system() == 'Windows':
        host = "mme"
        s = Server(duplex=0)
        s.reinit(buffersize=1024, duplex=0, winhost=host)
        s.boot()
        s.start()
    if platform.system() == 'Linux':
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
    ok_data = my_dlg.show()
    if my_dlg.OK:
        print(ok_data)
    else:
        print('user cancelled')
    participant_number = ok_data[0]
    return participant_number

participant_number = get_participant_number()
os.path.isdir("results") or os.mkdir("results")
results_directory = os.path.join("results", str(participant_number).zfill(3))
os.path.isdir(results_directory) or os.mkdir(results_directory)
results_file = str(participant_number).zfill(3) + "_results.dlm"
results_path = os.path.join(results_directory, results_file)
trial_info_header = "participant\tblock\ttrl\tprebeep\tbeep1\tinterbeep\tbeep2\tpostbeeps\n"
with open(results_path, "a") as f:
    f.write(trial_info_header)
win = make_window()
beep = sound.Sound(1000.0, secs=0.01, sampleRate=44100, stereo=True)
beep.setVolume(0.3)
number_of_trials = 160
break_trials = [39, 79, 119]
silence_before_beeps = 2.000
beep_duration = 0.010  # Laura = 0.010 as of 23 May (was previously 0.040)
silence_between_beeps = 0.500
min_duration = 6.0  # Laura = 6 seconds
max_duration = 8.0  # Laura = 8 seconds
block_number = 1
press_any_key_when_ready(win)
for t in range(number_of_trials):

    do_fix_cross(win)

    #parallel_port.setData(0)

    time.sleep(silence_before_beeps)

    beep_number = 1
    trigger_code = (beep_number*10) + block_number
    beep1on = time.time()
    #parallel_port.setData(trigger_code)
    beep.play()
    time.sleep(beep_duration)
    beep1off = time.time()

    time.sleep(silence_between_beeps)

    beep_number = 2
    trigger_code = (beep_number * 10) + block_number
    beep2on = time.time()
    #parallel_port.setData(trigger_code)
    beep.play()
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

    trial_info = "{}\t{}\t{:3s}\t{}\t{:.12f}\t{}\t{:.12f}\t{}".format(participant_number, block_number, str(t+1).zfill(3), 1000.0*silence_before_beeps, 1000.0*(beep1off-beep1on), 1000.0*silence_between_beeps, 1000.0*(beep2off-beep2on), 1000.0*post_beep_silence_dur)

    print(trial_info)
    
    with open(results_path, "a") as f:
        f.write(trial_info+"\n")

    if t in break_trials:
        take_a_break(win)
        block_number += 1

# number_of_trials has been reached
s.stop()
win.close()
core.quit()
