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


sudo apt-get install libjack-jackd2-dev libportmidi-dev portaudio19-dev liblo-dev libsndfile-dev
sudo apt-get install python3-dev python3-tk python3-pil.imagetk python3-pip
git clone https://github.com/belangeo/pyo.git
cd pyo
sudo python3 setup.py install --install-layout=deb --use-jack --use-double

#If you want to be able to use all of pyo’s gui widgets, you will need wxPython-phoenix.

#    Install requirements outlined in the README.rst at https://github.com/wxWidgets/Phoenix/blob/master/README.rst
#    Install wxPython with pip:

sudo pip3 install -U wxPython


or

In the ./scripts folder, there is some alternate scripts to simplify the compilation process a little bit. These scripts will compile pyo for the version of python pointed to by the command python.

To compile both 32-bit and 64-bit resolutions on linux with jack support:

sudo sh scripts/compile_linux_withJack.sh

