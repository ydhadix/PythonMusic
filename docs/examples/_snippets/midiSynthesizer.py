# midiSynthesizer.py
#
# Create a simple MIDI synthesizer which plays notes originating
# on a external MIDI controller.  More functionality may be easily
# added.
#

from midi import *
from music import *

# select input MIDI controller
midiIn = MidiIn()

# create callback function to start notes
def beginNote(eventType, channel, data1, data2):

   # start this note on internal MIDI synthesizer
   Play.noteOn(data1, data2, channel)
   #print "pitch =", data1, "volume =", data2

# and register it
midiIn.onNoteOn(beginNote)

# create callback function to stop notes
def endNote(eventType, channel, data1, data2):

   # stop this note on internal MIDI synthesizer
   Play.noteOff(data1, channel)
   #print "pitch =", data1, "volume =", data2

# and register it
midiIn.onNoteOff(endNote)

# done!