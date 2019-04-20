#!/home/matt/anaconda3/bin/python3.7

# from pyo import *
# import random
# s = Server(duplex=0)
# s.setOutputDevice(0)
# s.boot()
# s.start()
# # fr = Sig(value=400)
# fr = Sig(value=1000)
# # p = Port(fr, risetime=0.001, falltime=0.001)
# p = Port(fr, risetime=0.1, falltime=0.1)
# a = SineLoop(freq=p, mul=.5).out()
# # a = SineLoop(freq=p, feedback=0.08, mul=.3).out()
# # b = SineLoop(freq=p*1.005, feedback=0.08, mul=.3).out(1)
# def pick_new_freq():
#     pass
# #     fr.value = random.randrange(300,601,50)
# #     # fr.value = 400.0
# # pat = Pattern(function=pick_new_freq, time=0.5).play()
# pat = Pattern(function=pick_new_freq, time=1.0).play()
# time.sleep(2)


import pyo
import time
# s = Server(sr=512, duplex=0, audio='jack', nchnls=1)
s = pyo.Server(sr=48000, nchnls=2, buffersize=2048, duplex=0, audio='jack', jackname='pyo')
s.setOutputDevice(0)
s.boot()
s.start()
# s.setGlobalDur(0.04)
sine = pyo.Sine(freq=1000).play()
# sine_out = sine.out()
# fol2 = Follower2(sine_out, risetime=0.004, falltime=.004, mul=1)
# fol2.out()
# time.sleep(1)
for trial in range(3):
    time.sleep(0.1)
    sine.out(dur=0.04)
#    time.sleep(0.04)

#s.gui(locals())
# time.sleep(1)

# n = fol2.out(dur=0.04)
# p = n.play(dur=0.04)
# time.sleep(2)


# from pyo import *
# import time
# s = Server(duplex=0)
# s.setOutputDevice(0)
# s.boot()
# s.start()
# lfo = Sine(.25, 0, .1, .1)
# a = SineLoop(freq=[400,500], feedback=lfo, mul=.2)
# a.out()
# time.sleep(1)
#
