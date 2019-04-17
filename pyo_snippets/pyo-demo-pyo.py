#!/usr/bin/env python

from pyo import *
import time

s = Server(duplex=0)
s.setOutputDevice(0)
s.boot()
s.start()
print('ok')
sf = SfPlayer("../sounds/lijffijt_40ms_90dB_1000Hz_4ms_rise_fall.wav", speed=1, loop=True).out()
# either
time.sleep(1) # to hear the sound for 1 second if running non-interactively from a script
# or
# s.gui(locals())  # to hear the sound until you press stop, by dint of playing it in a gui, if running non-interactively from a script
s.stop()
