from pyo import *
s = Server().boot()
s.start()
sf = SfPlayer("click_20ms.wav", speed=1, loop=True).out()
