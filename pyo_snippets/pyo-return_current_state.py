#!/usr/bin/env python

from pyo import *

print("\n\n")

# print("Audio host APIS:")
pa_list_host_apis()
pa_list_devices()
i = pa_get_default_input()
o = pa_get_default_output()

print("\n\n")

print("Default input device: %i" % i)
print("Default output device: %i" % o)



