#!/usr/bin/env bash

# See http://ajaxsoundstudio.com/pyodoc/compiling.html

# ensure we have the dependencies
sudo apt-get install libjack-jackd2-dev libportmidi-dev portaudio19-dev liblo-dev libsndfile-dev
sudo apt-get install python3-dev python3-tk python3-pil.imagetk python3-pip
# work from /home/matt
cd /home/matt
# grab pyo sources from github
git clone https://github.com/belangeo/pyo.git
# change permissions to matt:matt for pyo source
sudo chown -R matt:matt /home/matt/pyo
# change wd to pyo source
cd /home/matt/pyo
# Remove build directory if exist
if cd build; then
    echo
    echo "********** Removing older build directory **********"
    cd ..
    sudo rm -rf build
fi

echo
echo "**************************************************"
echo "****************** build library *****************"
echo "**************************************************"
echo

# use anaconda3 python, assuming that 'which python' points to that
which python
# To compile both 32-bit and 64-bit resolutions on linux with jack support:
python setup.py install --use-double --use-jack
