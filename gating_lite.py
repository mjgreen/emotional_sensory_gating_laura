import os
import datetime
import random
import shutil
import sys
import time
# import pandas as pd
import io
from contextlib import redirect_stdout
with redirect_stdout(io.StringIO()): import psychopy
from psychopy import logging, prefs
logging.console.setLevel(logging.INFO)  # get messages about the sound lib as it loads
sound_device_list = ["sounddevice", "pyo", "pygame", "pysoundcard"]
sound_device_list = ["pyo", "sounddevice", "pygame", "pysoundcard"]
prefs.hardware['audioLib'] = sound_device_list
from psychopy import sound, core
sound_info = 'Using %s (with %s) for sounds' % (sound.audioLib, sound.audioDriver)
print(sound_info)
beep = sound.Sound('sounds/lijffijt_40ms_90dB_1000Hz_4ms_rise_fall.wav')


def sound_trial(sound_type=None, trial_type_name=None, trial_number=0, n_trials=0, trial_initial_silence=0.0, trial_final_silence=0.0, sound_durations=[]):
    t0 = core.getTime()
    # core.wait(trial_initial_silence)
    sound_type.play()
    # core.wait(0.5)
    # sound_type.play()
    t1 = core.getTime()
    # core.wait(secs=trial_final_silence)
    return t0, t1


trial_order = ['beep' for n in range(10)]  #'['beep', 'beep', 'beep', 'beep']
msg = '\ntrial order is %s; sound device is %s, driver is %s\n' % (trial_order, sound.audioLib, '\"probably portaudio\"' if not sound.audioDriver else sound.audioDriver)
print(msg)

# trial sequence
num_trials = len(trial_order)
sound_durs = []
core.wait(1)
for trial in range(len(trial_order)):  # trial_order:
    trial_type = trial_order.pop(0)
    # print("starting trial {} of {} at {}".format(trial + 1, num_trials, core.getTime()))
    t0, t1 = sound_trial(sound_type=beep if trial_type == 'beep' else None, trial_type_name=trial_type, trial_number=trial, n_trials=num_trials,
                             trial_initial_silence=2.0, trial_final_silence=random.uniform(6.0, 8.0), sound_durations = sound_durs)
    print("trial {} time should be 40:\t{}".format( trial+1, (t1 - t0) * 1000.0))
    core.wait(1)

print('the end\n')
