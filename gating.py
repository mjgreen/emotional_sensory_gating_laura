import os
import datetime
import random
import shutil
import sys
import pandas as pd
from psychopy import visual, core, event, gui, parallel, logging, prefs
logging.console.setLevel(logging.DEBUG)  # get messages about the sound lib as it loads
prefs.hardware['audioLib'] = ['pyo']  # 'sounddevice', 'pyo', 'pygame'
from psychopy import sound
print('Using %s (with %s) for sounds' % (sound.audioLib, sound.audioDriver))

os.path.exists('/tmp/runtime-root') or os.mkdir('/tmp/runtime-root')

# offer as this session's participant number the last participant's number plus 1
os.path.exists("results") or os.makedirs("results")
maximum_subject_number_in_results_dir = []
last_participant_number = 0
results_files_so_far = [f for f in os.listdir("results")]
if results_files_so_far:
    for this_participant in range(len(results_files_so_far)):
        maximum_subject_number_in_results_dir.append((100 * int(results_files_so_far[this_participant][1])) + (10 * int(results_files_so_far[this_participant][2])) + (1 * int(results_files_so_far[this_participant][3])))
    last_participant_number = max(maximum_subject_number_in_results_dir)
suggest_this_participant_number = last_participant_number + 1

# handle the gui
dialog = gui.Dlg(title="Enter session information")
dialog.addFixedField("Session timestamp:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
dialog.addField("Participant Number:", suggest_this_participant_number)
dialog.addField("Order of mood induction:", choices=['angry then neutral', 'neutral then angry'])
ok_data = dialog.show()
if dialog.OK:
    dlg = {dialog.__dict__["inputFieldNames"][i]: dialog.__dict__["data"][i] for i in range(len(dialog.__dict__["data"]))}
else:
    print("quitting because user pressed cancel at the dialogue")
    core.quit()

# pull variables from the gui
session_timestamp = dlg["Session timestamp:"]
participant_number = dlg["Participant Number:"]
mood_order_response = dlg["Order of mood induction:"]
mood_order = ["angry", "neutral"] if mood_order_response == 'angry then neutral' else ["neutral", "angry"]

# handle the results directory
results_directory = os.path.join('results', 'P'+str(participant_number).zfill(3))
if participant_number == 0 and os.path.exists(results_directory):
    shutil.rmtree(results_directory)
os.path.exists(results_directory) or os.makedirs(results_directory)

# One of the blocks should have 5 click trials (out of 80) and the other should have 4 click trials (out of 80),
# but we don't want to systematically have angry with 5 and neutral with 4 or the other way around,
# so flip a coin to decide which block gets 4 clicks and which gets 5 clicks
sound_list_4_clicks = ['click' for sound in range(4)] + ['beep' for sound in range(76)]
random.shuffle(sound_list_4_clicks)
sound_list_5_clicks = ['click' for sound in range(5)] + ['beep' for sound in range(75)]
random.shuffle(sound_list_5_clicks)
coin_flip = random.sample(['heads', 'tails'], 1)[0]
sound_list = sound_list_4_clicks + sound_list_5_clicks if coin_flip == 'heads' else sound_list_5_clicks + sound_list_4_clicks  # sound_list has length 160

# prepare list of trials, length 160, which is one full session made of 2 blocks of 80 trials
n_blocks = 2
n_trials_per_block = 80
trial_dict = {}
for bk in range(1, n_blocks + 1):
    for tr in range(1, n_trials_per_block + 1):
        instance = tr + ((bk - 1) * n_trials_per_block)
        trial_dict[instance] = {
            'participant_id': participant_number,
            'session_timestamp': session_timestamp,
            'unique_id': instance,
            'block_number': bk,
            'trial_number': tr,
            'mood_level': mood_order[bk-1],
            'sound_type': sound_list[instance-1]
        }

# print(trial_dict[0])  # is a key error - the dict of dicts is indexed by the name of the dict for that row: the name of the first row is 1

# write trial_dict to excel
temp = pd.DataFrame.from_dict(trial_dict, orient='columns')
temp = temp.transpose()
# print(temp.to_string(header=True, index=False, index_names=False, col_space=13, columns=['participant_id', 'session_timestamp', 'unique_id', 'block_number', 'trial_number', 'mood_level', 'sound_type']))
writer = pd.ExcelWriter(os.path.join(results_directory, "P" + str(participant_number).zfill(3) + "_trials.xlsx"), engine='xlsxwriter')
temp.to_excel(writer, str(participant_number), index=False, columns=['participant_id', 'session_timestamp', 'unique_id', 'block_number', 'trial_number', 'mood_level', 'sound_type'])
writer.save()

# win = visual.Window(monitor="testMonitor")  # on linux
win = visual.Window(monitor="monitor_eeg", autoLog=True, winType='pygame')  # on linux after putting that file monitor_eeg.json in ~/.psychopy3/monitors (not having hacked calibTools.py)
#                                                                           # winType defaults to 'pyglet' if unspecified
#                                                                           # autoLog=True spells out the window specs in the log-to-console
# win = visual.Window()  # on windows

# load the sounds
beep = sound.Sound('beep_20ms.wav')
click = sound.Sound('click_20ms.wav')

# trial sequence
for bk in range(1, n_blocks+1):
    for tr in range(1, n_trials_per_block + 1):
        instance = tr + ((bk - 1) * n_trials_per_block)
        sound_type = trial_dict[instance]['sound_type']
        # (A) 2 seconds of silence
        core.wait(2)
        # (B) play sound first time
        if sound_type == 'beep':
            beep.play()
        elif sound_type == 'click':
            click.play()
        # (C) 500ms of silence
        core.wait(0.5)
        # (D) play sound second time
        if sound_type == 'beep':
            beep.play()
        elif sound_type == 'click':
            click.play()
        # (E) silence for random float between 5.0 seconds and 8.0 seconds
        core.wait(secs=random.uniform(5.0, 8.0))
        k = event.getKeys(keyList='escape')
        if k:
            print('quitting')
            core.quit()
        else:
            pass
