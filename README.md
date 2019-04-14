# Ubuntustudio
default install

`apt install xscreensaver` (to easily permit resume from lockced screen which is botched by default)

# Laura RV's emotional sensory gating experiments

Task: listen to the sounds. If the sounds are beeps, do nothing. If the sounds are clicks, press the space bar.

Trial sequence: { | 2000ms | sound | 500ms | sound | random(min=5000ms, max=8000ms) during which permit subject to press spacebar if the sounds were clicks | }

Experiment structure: 2 * (mood induction > block of trials). The mood induction is done as an offline pen and paper exercise. There are 2 levels of mood induction, anger; neutral. The order of (A) angry > trials; (B) neutral > trials is randomised between subjects so that some get A > B and others get B > A. A block is 80 trials. There is a rest after 40 trials. In one block there should be 76 trials where the sounds are both beeps, and 4 trials where the sounds are both clicks. The other block should have 75 trials where the sounds are both beeps and 5 trials where the sounds are both clicks. 

The beeps should be as below: Square waves; intensity, 70dB, frequency, 1,000 Hz; duration, 1ms including 10% rise/fall envelope. Clicks can be anything, 1ms duration but sounding quite different from the beeps.

# psychopy.sound - play various forms of sound
Sound

PsychoPy currently supports a choice of three sound libraries: pyo, sounddevice or pygame. Select which will be used via the audioLib preference. sound.Sound() will then refer to one of SoundDevice SoundPyo or SoundPygame. This can be set on a per-experiment basis by importing preferences, and setting the audioLib option to use.

* The pygame backend is the oldest and should always work without errors, but has the least good performance. Use it if latencies foryour audio don’t mattter. {__MJG: yep, pygame seems to work. But not suitable for EEG if the timing is botched like Jon says here__}
* The pyo library is, in theory, the highest performer, but in practice it has ften had issues (at least on macOS) with crashes and freezing of experiments, or causing them not to finish properly. If those issues aren’t affecting your studies then this could be the one for you. {__MJG: pyo seems to be reliable if you can get it installed properly -- the best  way seems to be to satisfy dependencies from apt or sources (especially source for portaudio, configured with --with-alsa --with-jack --enable-debug-output) and then use pip to install from github: `pip install git+git://github.com/belangeo/pyo.git`__}
* The sounddevice library looks like the way of the future. The performance appears to be good (although this might be less so in cases where you have complex rendering being done as well because it operates from the same computer core as the main experiment code). It’s newer than pyo and so more prone to bugs and we haven’t yet added microphone support to record your participants. {__MJG: it often core dumps though, but it does work if it doesn't core dump, so it's not that it is completely botched, just not reliable enough for an experiment.__}
