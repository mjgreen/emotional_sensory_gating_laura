lib = ['pygame']
lib = ['sounddevice']
lib = ['pyo']

from psychopy import prefs
prefs.hardware['audioLib'] = lib
from psychopy import sound
print(sound.audioLib)

