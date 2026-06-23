# sineMelodyPlus.py
#
# This program demonstrates how to create a melody from a sine wave.
# It maps the sine function to several musical parameters, i.e.,
# pitch contour, duration, dynamics (volume), and panning.
#

from music import *
from math import *

sineMelodyPhrase = Phrase()
density = 25.0                 # higher for more notes in sine curve
cycle = int(2 * pi * density)  # steps to traverse a complete cycle

# create one cycle of the sine curve at given density
for i in range(cycle):
   value = sin(i / density)    # calculate the next sine value
   pitch = mapValue(value, -1.0, 1.0, C2, C8)   # map to range C2-C8
   #duration = TN
   duration  = mapValue(value, -1.0, 1.0, TN, SN)   # map to TN-SN
   dynamic = mapValue(value, -1.0, 1.0, PIANISSIMO, FORTISSIMO)
   panning = mapValue(value, -1.0, 1.0, PAN_LEFT, PAN_RIGHT)

   note = Note(pitch, duration, dynamic, panning)
   sineMelodyPhrase.addNote(note)

View.pianoRoll(sineMelodyPhrase)
Play.midi(sineMelodyPhrase)