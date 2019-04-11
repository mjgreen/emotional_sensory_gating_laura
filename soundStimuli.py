#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sound stimuli are currently an area of development in PsychoPy

Previously we used pygame. Now the pyo library is also supported.
On OSX this is an improvement (using coreaudio rather than SDL).
On windows this should help on systems with good sound cards,
but this is yet to be confirmed.

See the demo hardware > testSoundLatency.py
"""
import sys
from psychopy import logging, prefs, core
logging.console.setLevel(logging.DEBUG)  # get messages about the sound lib as it loads
# prefs.hardware['audioLib'] = ['pygame']
# prefs.hardware['audioLib'] = ['sounddevice']
prefs.hardware['audioLib'] = ['pyo']
from psychopy import sound
print('Using %s (with %s) for sounds' % (sound.audioLib, sound.audioDriver))

mybeep = sound.Sound('beep_20ms.wav')
myclick = sound.Sound('click_20ms.wav')

core.wait(1)

mybeep.play()
core.wait(.5)

myclick.play()
core.wait(.5)

print('finished')
core.quit()

