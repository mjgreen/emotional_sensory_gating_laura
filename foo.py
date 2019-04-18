import time
from pyo import *
s = Server().boot()
s.start()
sine = Sine(freq=1000, mul=.2).out(dur=.04)
time.sleep(0.040)
s.stop()
time.sleep(0.25)