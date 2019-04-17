# Ubuntustudio
default install

`apt install xscreensaver` (to easily permit resume from loccked screen which is botched by default)

# Laura RV's emotional sensory gating experiments

Task: listen to the sounds. 

# psychopy.sound - play various forms of sound
Sound

PsychoPy currently supports a choice of three sound libraries: pyo, sounddevice or pygame. Select which will be used via the audioLib preference. sound.Sound() will then refer to one of SoundDevice SoundPyo or SoundPygame. This can be set on a per-experiment basis by importing preferences, and setting the audioLib option to use.

* The pygame backend is the oldest and should always work without errors, but has the least good performance. Use it if latencies foryour audio don’t mattter. {__MJG: yep, pygame seems to work. But not suitable for EEG if the timing is botched like Jon says here__}
* The pyo library is, in theory, the highest performer, but in practice it has often had issues (at least on macOS) with crashes and freezing of experiments, or causing them not to finish properly. If those issues aren’t affecting your studies then this could be the one for you. {__MJG: pyo seems to be reliable if you can get it installed properly -- the best  way seems to be to satisfy dependencies from apt or sources (especially source for portaudio, configured with --with-alsa --with-jack --enable-debug-output) and then use pip to install from github: `pip install git+git://github.com/belangeo/pyo.git`__}
* The sounddevice library looks like the way of the future. The performance appears to be good (although this might be less so in cases where you have complex rendering being done as well because it operates from the same computer core as the main experiment code). It’s newer than pyo and so more prone to bugs and we haven’t yet added microphone support to record your participants. {__MJG: it often core dumps though, but it does work if it doesn't core dump, so it's not that it is completely botched, just not reliable enough for an experiment.__}

# pyo installation 

Using pip, if you have sorted all the dependencies. Not the best way in my experience.

```bash
pip install git+git://github.com/belangeo/pyo.git
```

Using `apt`, `git`, and `python setup.py install` (this has worked for me, at least on ubuntustudio)


```bash
#!/usr/bin/env bash

# See http://ajaxsoundstudio.com/pyodoc/compiling.html

# ensure we have the dependencies
sudo apt-get install libjack-jackd2-dev libportmidi-dev portaudio19-dev liblo-dev libsndfile-dev
sudo apt-get install python3-dev python3-tk python3-pil.imagetk python3-pip
# wxPython is optional
pip install wxPython # or use a wheel
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
```