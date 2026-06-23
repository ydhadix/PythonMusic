# midiSynthesizer2.py
#
# Create a simple MIDI synthesizer which plays notes originating
# on a external MIDI controller.  This version includes a way
# to change MIDI sounds (instruments), by turning one of the
# controller knobs.
#

from midi import *
from music import *

# knob for changing instruments (same as data1 value sent when
# turning this knob on the MIDI controller)
knob = 16

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

# create callback function to change instrument
def changeInstrument(eventType, channel, data1, data2):

   if data1 == knob:   # is this the instrument knob?

      # set the new instrument in the internal synthesizer
      Play.setInstrument(data2)

      # output name of new instrument (and its number)
      print('Instrument set to "' + MIDI_INSTRUMENTS[data2] + \
            ' (' + str(data2) + ')"')

# and register it (only for 176 type events)
midiIn.onInput(176, changeInstrument)

# hide messages received by MIDI controller
midiIn.hideMessages()