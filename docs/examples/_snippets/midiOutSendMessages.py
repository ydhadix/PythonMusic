# midiOut.py
#
# Demonstrates how to send arbitrary messages to an external MIDI device.
#

from midi import *

midiOut = MidiOut()

# send message for "All Notes Off" to all channels
for channel in range(16):  # cycle through all channels

   # send message for "All Notes Off" on current channel
   midiOut.sendMidiMessage(176, channel, 123, 0)