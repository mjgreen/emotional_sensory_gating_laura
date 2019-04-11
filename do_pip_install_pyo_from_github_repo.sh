#!/usr/bin/env bash

# Not installing portaudio19-dev because I installed portaudio from source this time
#sudo apt install libsndfile-dev portaudio19-dev  # this pulls in jack0 and jack1 things and removes jack2 things

pip install git+git://github.com/belangeo/pyo.git  # Successfully installed pyo-0.9.2

## files are:
#/home/matt/anaconda3/lib/python3.7/site-packages/pyo-0.9.2.dist-info
#/home/matt/anaconda3/lib/python3.7/site-packages/pyo

## previously, what I got from apt install python3-pyo was these files:
#/usr/lib/python3/dist-packages/pyo.py
#/usr/lib/python3/dist-packages/pyo64.py
#/usr/lib/python3/dist-packages/pyolib
#/usr/lib/python3/dist-packages/pyo-0.9.1.egg-info
