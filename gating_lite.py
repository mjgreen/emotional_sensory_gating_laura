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
logging.console.setLevel(logging.DEBUG)  # get messages about the sound lib as it loads
sound_device_list = ["sounddevice", "pygame", "pyo", "pysoundcard"]
prefs.hardware['audioLib'] = sound_device_list
from psychopy import sound, core
sound_info = 'Using %s (with %s) for sounds' % (sound.audioLib, sound.audioDriver)
# logging.info(msg=sound_info)

# load the sounds
beep = sound.Sound('beep_20ms.wav')
clik = sound.Sound('click_20ms.wav')


def sound_trial(sound_type=None, trial_type=None):
    print("psychopy sound info: {} {}".format(trial_type, sound_type))
    core.wait(2.0)
    sound_type.play()
    core.wait(0.5)
    sound_type.play()
    core.wait(secs=random.uniform(5.0, 8.0))


trial_order = random.sample([['beep', 'clik'], ['clik', 'beep']], 1)[0]
sound_device = sound.audioLib
msg = 'trial order is %s; sound device is %s' % (trial_order, sound_device)
print(msg)
for trial in range(len(trial_order)):  # trial_order:
    trial_type = trial_order.pop(0)
    sound_trial(sound_type=clik if trial_type == 'clik' else beep if trial_type == 'beep' else None, trial_type=trial_type)
