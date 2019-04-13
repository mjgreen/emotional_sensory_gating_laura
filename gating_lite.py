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
sound_device_list = ["pyo", "pysoundcard", "sounddevice", "pygame"]
prefs.hardware['audioLib'] = sound_device_list
from psychopy import sound, core
sound_info = 'Using %s (with %s) for sounds' % (sound.audioLib, sound.audioDriver)
# logging.info(msg=sound_info)

# load the sounds
beep = sound.Sound('beep_20ms.wav')
click = sound.Sound('click_20ms.wav')


def sound_trial(sound_type=None):
    if sound_type is None:
        return False
    this_sound = click if trial_type == 'click' else beep
    core.wait(2)
    this_sound.play()
    core.wait(0.5)
    this_sound.play()
    core.wait(secs=random.uniform(5.0, 8.0))


trial_order = random.sample([['beep', 'click'], ['click', 'beep']], 1)[0]
msg = 'trial order is %s' % trial_order
print(msg)
logging.info(msg)
for t in trial_order:
    trial_type = trial_order.pop(0)
    sound_trial(sound_type=trial_type)
