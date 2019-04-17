import os
import datetime
import random
import shutil
import sys
# import pandas as pd
import io
from contextlib import redirect_stdout
with redirect_stdout(io.StringIO()): import psychopy
from psychopy import logging, prefs
logging.console.setLevel(logging.INFO)  # get messages about the sound lib as it loads
sound_device_list = ["sounddevice", "pygame", "pyo", "pysoundcard"]
prefs.hardware['audioLib'] = sound_device_list
from psychopy import sound, core
sound_info = 'Using %s (with %s) for sounds' % (sound.audioLib, sound.audioDriver)
# logging.info(msg=sound_info)

# print(sound)

# load the sounds
beep = sound.Sound('beep_20ms.wav')
clik = sound.Sound('click_20ms.wav')


def sound_trial(sound_type=None, trial_type_name=None, trial_number=0, n_trials=0):
    trial_initial_silence = 2.0  # seconds
    trial_final_silence = random.uniform(5.0, 8.0)  # seconds
    print("starting trial {} of {}".format(trial_number+1, n_trials+1))
    print("trial initial silence for {} seconds".format(round(trial_initial_silence, 1)))
    core.wait(trial_initial_silence)
    print("about to play the first {}".format(trial_type_name))
    sound_type.play()
    core.wait(0.5)
    print("about to play the second {}".format(trial_type_name))
    sound_type.play()
    print("trial final silence for {} seconds".format(round(trial_final_silence, 1)))
    core.wait(secs=trial_final_silence)


trial_order = random.sample([['beep', 'click'], ['click', 'beep']], 1)[0]
sound_device = sound.audioLib
sound_driver = sound.audioDriver
msg = 'trial order is %s; sound device is %s driver = %s' % (trial_order, sound_device, sound_driver)
print(msg)

# trial sequence
for trial in range(len(trial_order)):  # trial_order:
    trial_type = trial_order.pop(0)
    sound_trial(sound_type=clik if trial_type == 'click' else beep if trial_type == 'beep' else None, trial_type_name=trial_type, trial_number=trial, n_trials=len(trial_order))
