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


def sound_trial(sound_type=None, trial_type_name=None, trial_number=0, n_trials=0, trial_initial_silence=0.0, trial_final_silence=0.0):
    # trial_initial_silence = 2.0  # seconds
    # trial_final_silence = random.uniform(1.0, 1.0)  # seconds  random.uniform(5.0, 8.0)
    print("starting trial {} of {}, a {} trial".format(trial_number+1, n_trials, trial_type))
    print("{} seconds silence".format(round(trial_initial_silence, 1)))
    core.wait(trial_initial_silence)
    print("{} # 1".format(trial_type_name))
    sound_type.play()
    core.wait(0.5)
    print("{} # 2".format(trial_type_name))
    if trial_type == 'beep':
        beep2.play()
    else:
        sound_type.play()
    print("{} seconds silence\n".format(round(trial_final_silence, 1)))
    core.wait(secs=trial_final_silence)


trial_order = random.sample([['beep', 'click'], ['click', 'beep']], 1)[0]
for times in range(4):
    trial_order = trial_order + random.sample([['beep', 'click'], ['click', 'beep']], 1)[0]
# trial_order = [random.sample([['beep', 'click'], ['click', 'beep']], 1)[0] for t in range(4)]
msg = '\ntrial order is %s; sound device is %s, driver is %s\n' % (trial_order, sound.audioLib, '\"probably portaudio\"' if not sound.audioDriver else sound.audioDriver)
print(msg)

# trial sequence
num_trials = len(trial_order)
for trial in range(len(trial_order)):  # trial_order:
    trial_type = trial_order.pop(0)
    # load the sounds here, else volume < 1.0 progressively makes the sound quieter every time it is .play()ed
    beep = sound.Sound('beep_20ms.wav', volume=0.4)
    beep2 = sound.Sound('beep_20ms.wav', volume=0.4)
    clik = sound.Sound('click_20ms.wav', volume=1.0)
    # go for trial
    sound_trial(sound_type=clik if trial_type == 'click' else beep if trial_type == 'beep' else None, trial_type_name=trial_type, trial_number=trial, n_trials=num_trials,
                trial_initial_silence=2.0, trial_final_silence=random.uniform(5.0, 8.0))

print('the end\n')