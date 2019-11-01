"""
python3 appears to work, but that's not to say you cant run it in python2
EEG lab's Psychopy3 seems to be python3, when laura phoned me from the lab, that's what the 'shell' tab said
"""

import time
import random
import gc
import os
import platform
from psychopy import visual, event
from psychopy import logging, prefs, monitors, gui, parallel
logging.console.setLevel(logging.DEBUG)
prefs.hardware['audioLib'] = ['pygame']
from psychopy import sound, core
print('Using %s for sounds' % sound.audioLib)
logging.console.setLevel(logging.ERROR)

def make_window():
    viewpixx = monitors.Monitor("eeg", width=54, distance=53)
    viewpixx.setSizePix((1920, 1080))
    viewpixx.saveMon()
    monitor = viewpixx
    which_screen = 1
    print("using {} monitor".format(monitor.name))
    xpx = monitor.getSizePix()[0]
    ypx = monitor.getSizePix()[1]
    # xcm = monitor.getWidth()
    win = visual.Window(fullscr=True, size=[xpx, ypx], units='pix', allowGUI=False, waitBlanking=True, color=[.1, .1, .1], monitor=monitor.name, screen=which_screen, winType=None)
    actual_frame_rate = win.getActualFrameRate()
    print("actual frame rate: {} Hz".format(int(round(actual_frame_rate))))
    return win

def initial_instruction(win):
    instr = visual.TextStim(win=win, wrapWidth=1200, height=50, text="Your task is to listen to beeps. You do not need to do anything apart from keeping your eyes on the fixation cross. Please also relax as much as you can and do not move your head as we are recording what your brain is doing during this task.\n\nPress any key to start.")
    instr.draw()
    win.flip()
    event.waitKeys()
    win.flip()
    
def end_of_block_1(win):
    instr = visual.TextStim(win=win, wrapWidth=1200, height=50, text="Take a break. Press any key to start again")
    instr.draw()
    win.flip()
    event.waitKeys()
    win.flip()
    
def end_of_block_2(win):
    instr = visual.TextStim(win=win, wrapWidth=1200, height=50, text="Now the experimenter will come for the anger induction.")
    instr.draw()
    win.flip()
    event.waitKeys()
    instr = visual.TextStim(win=win, wrapWidth=1200, height=50, text="Press any key to start.")
    instr.draw()
    win.flip()
    event.waitKeys()
    
def end_of_block_3(win):
    instr = visual.TextStim(win=win, wrapWidth=1200, height=50, text="Now for the next minute, please recall your angry scenario, remember how angry you felt at the time, and how angry you feel now.")
    instr.draw()
    win.flip()
    core.wait(60)
    instr = visual.TextStim(win=win, wrapWidth=1200, height=50, text="Press any key to start.")
    instr.draw()
    win.flip()
    event.waitKeys()
    win.flip()

def do_fix_cross(win):
    extent = 20
    fixation = visual.ShapeStim(win, vertices=((0, -extent), (0, extent), (0, 0), (-extent, 0), (extent, 0)), lineWidth=6, closeShape=False, lineColor="black", autoLog=False)
    fixation.draw()
    win.flip()

def start_sound_server():
    s = None
    if platform.system() == 'Windows':
        host = "asio"
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

def graceful_exit(s, win):
    s.stop()
    win.close()
    core.quit()

def get_participant_number():
    my_dlg = gui.Dlg(title="gating")
    my_dlg.addField('Participant number:', 999)
    my_dlg.addField('parallel port?', initial=True)
    ok_data = my_dlg.show()
    if my_dlg.OK:
        print(ok_data)
    else:
        print('user cancelled')
    participant_number = ok_data[0]
    there_is_a_parallel_port = ok_data[1]
    return participant_number, there_is_a_parallel_port

# raise thread priority
core.rush(True)

# garbage collection off
gc.disable()

participant_number, there_is_a_parallel_port = get_participant_number() # this calls the gui
if there_is_a_parallel_port:
    parallel_port = parallel.ParallelPort(address=0x1FF8)  # eeg z440
else:
    parallel_port = None

os.path.isdir("results") or os.mkdir("results")
results_directory = os.path.join("results", str(participant_number).zfill(3))
os.path.isdir(results_directory) or os.mkdir(results_directory)
results_file = str(participant_number).zfill(3) + "_results.dlm"
results_path = os.path.join(results_directory, results_file)
trial_info_header = "participant\tblock\ttrl\tprebeep\tbeep1\tinterbeep\tbeep2\tpostbeeps\n"
with open(results_path, "a") as f:
    f.write(trial_info_header)
win = make_window()
beep_duration = 0.010  # Laura = 0.010 as of 23 May (was previously 0.040)
beep = sound.Sound(2000.0, secs=beep_duration, sampleRate=44100, stereo=True)
beep.setVolume(1.0)

''' insert a bit before ethe trials start, a bit like a practice block but not really, 
whose purpose is to test volume level and permit the experimenter to repeat until they are happy with the volume '''
# Laura: "Have a practice block with a few beeps close together (no need to wait 6-10 minutes) to test the volume.
#         Maybe 5 beeps 1 second apart, with the option to start that block again if needed?"

volume_test_start = visual.TextStim(win=win, wrapWidth=1200, height=25,
                                      text='Before the experiment starts we test the volume level. \n\n'
                                           'When you dismiss this message, you will hear 5 beeps 1 second apart. '
                                           'Then you will be asked whether you want to continue with the experiment: '
                                           'If you are happy with the volume, press "y", or if you want to change the volume level and repeat the process, press "n". \n\n'
                                           'Press any key now to dismiss the message and play the beeps')
volume_test_during = visual.TextStim(win=win, wrapWidth=1200, height=25, text='The beeps are playing now: fiddle with the volume until you are happy with it')
volume_test_after = visual.TextStim(win=win, wrapWidth=1200, height=25, text='Was the volume ok? Press y for yes or n for no')

volume_ok = False
while not volume_ok:
    volume_test_start.draw()
    win.flip()
    event.waitKeys()

    volume_test_during.draw()
    win.flip()

    for beeps in range(5):
        beep.play()
        time.sleep(beep_duration)
        core.wait(1)

    volume_test_after.draw()
    win.flip()
    k = event.waitKeys(keyList=['y','n'])
    if k[0] == 'y':
        volume_ok = True
    if k[0] == 'n':
        volume_ok = False

assert volume_ok
''' if we get here, it can only be because you pressed 'y' to say yes the volume was ok. If you had pressed 'n' to say no the volume was not ok, you'd still be in the while loop
If something unexpected happened, you'd be thrown out by the assertion error'''

number_of_trials = 160
break_trials = [39, 79, 119]
silence_before_beeps = 2.000
silence_between_beeps = 0.500
min_duration = 6.0
max_duration = 8.0
block_number = 1
initial_instruction(win)
for t in range(number_of_trials):

    do_fix_cross(win)

    if there_is_a_parallel_port: parallel_port.setData(0)

    time.sleep(silence_before_beeps)
    
    if there_is_a_parallel_port: parallel_port.setData(0)
    beep_number = 1
    trigger_code_1 = (block_number*10) + beep_number
    beep1on = time.time()
    if there_is_a_parallel_port: parallel_port.setData(trigger_code_1)
    beep.play()
    time.sleep(beep_duration)
    beep1off = time.time()
    if there_is_a_parallel_port: parallel_port.setData(0)

    time.sleep(silence_between_beeps)
    
    if there_is_a_parallel_port: parallel_port.setData(0)
    beep_number = 2
    trigger_code_2 = (block_number * 10) + beep_number
    beep2on = time.time()
    if there_is_a_parallel_port: parallel_port.setData(trigger_code_2)
    beep.play()
    time.sleep(beep_duration)
    beep2off = time.time()
    if there_is_a_parallel_port: parallel_port.setData(0)

    post_beep_silence_dur = random.uniform(min_duration, max_duration)
    t0 = core.getTime()
    while core.getTime() - t0 < post_beep_silence_dur:
        k = event.getKeys(keyList=['escape'])
        if k:
            print("quitting because experimenter pressed escape")
            win.close()
            core.quit()

    #trial_info = "{}\t{}\t{:3s}\t{}\t{:.3f}\t{}\t{:.3f}\t{}\t{}\t{}".format(participant_number, block_number, str(t+1).zfill(3), round(1000.0*silence_before_beeps,2), 1000.0*(beep1off-beep1on),2, round(1000.0*silence_between_beeps,2), 1000.0*(beep2off-beep2on), round(1000.0*post_beep_silence_dur,2), trigger_code_1, trigger_code_2)
    trial_info = "{}\t{}\t {}\t{}".format(participant_number, block_number, str(t+1).zfill(3), trigger_code_1, trigger_code_2)
    print(trial_info)
    
    with open(results_path, "a") as f:
        f.write(trial_info+"\n")

    #39, 79, 119
    if t == 39:
        block_number = block_number + 1
        end_of_block_1(win)
    if t == 79:
        block_number = block_number + 1
        end_of_block_2(win)
    if t == 119:
        block_number = block_number + 1
        end_of_block_3(win)
        

print("end of run")
# garbage collection on again
gc.enable()
# lower thread priority
core.rush(False)
# close window
win.close()
# stop sound server
s.stop()
# quit process
core.quit()
 
