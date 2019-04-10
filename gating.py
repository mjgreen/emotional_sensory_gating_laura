import os
import datetime
from psychopy import visual, core, event, gui, parallel

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
experiment_timestamp = dlg["Session timestamp:"]
participant_number = dlg["Participant Number:"]
mood_order_response = dlg["Order of mood induction:"]
mood_order = ["angry", "neutral"] if mood_order_response == 'angry then neutral' else ["neutral", "angry"]
