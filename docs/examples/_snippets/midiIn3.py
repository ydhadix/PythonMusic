# midiIn3.py
#
# Demonstrates how to see what type of messages a MIDI device generates.
#

from midi import *

midiIn = MidiIn()

def printEvent(event, channel, data1, data2):

   if event == 176:
      print("Got a program change (CC) message", "on channel", channel, "with data values", data1, data2)
   elif event == 144:
      print("Got a Note On message", "on channel", channel, "for pitch", data1, "and volume", data2)
   elif (event == 128) or (event == 144 and data2 == 0):
      print("Got a Note Off message", "on channel", channel, "for pitch", data1)
   else:
      print("Got another MIDI message:", event, channel, data1, data2)

midiIn.onInput(ALL_EVENTS, printEvent)

# since we have established our own way to process incoming messages,
# stop printing out info about every message
midiIn.hideMessages()