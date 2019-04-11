lib = ['pygame']
# lib = ['sounddevice']
# lib = ['pyo']

from psychopy import prefs
prefs.hardware['audioLib'] = lib
from psychopy import sound
print(sound.audioLib)


# from psychopy import prefs
# prefs.hardware['audioLib']=['pygame']
# from psychopy import sound
# sound.audioLib
#
# from psychopy import prefs
# prefs.hardware['audioLib']=['sounddevice']
# from psychopy import sound
# sound.audioLib
#
# from psychopy import prefs
# prefs.hardware['audioLib']=['pyo']
# from psychopy import sound
# sound.audioLib
