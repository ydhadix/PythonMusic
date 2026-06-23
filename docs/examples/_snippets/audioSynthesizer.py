# audioSynthesizer.py
#
# Create a simple AudioSample synthesizer which plays notes originating
# on a external MIDI controller.  More functionality may be easily
# added.
#

from midi import *
from music import *

# select input MIDI controller
midiIn = MidiIn()

# load sound
audio = AudioSample("strings - A4.wav", A4)

# create a nice envelope
env = Envelope([0, 20, 10], [0.0, 0.8, 1.0], 30, 0.6, 1200)
#env = Envelope()   # default

# create callback function to start notes
def beginNote(eventType, channel, data1, data2):

   # start this note, and loop it!!
   Play.audioOn(data1, audio, data2, 64, True, env)
   #print "pitch =", data1, "volume =", data2

# and register it
midiIn.onNoteOn(beginNote)

# create callback function to stop notes
def endNote(eventType, channel, data1, data2):

   # stop this note
   Play.audioOff(data1, audio, env)
   #print "pitch =", data1, "volume =", data2

# and register it
midiIn.onNoteOff(endNote)