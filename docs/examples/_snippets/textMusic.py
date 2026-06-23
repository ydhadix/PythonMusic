# textMusic.py
#
# It demonstrates one way to generate music from text.
#
# * Note pitch is based on the ASCII value of characters.
# * Note duration is selected from a weighted-probability list
#   (again, based on ASCII value).
# * Note dynamic is selected randomly.
#
# All other music parameters (panoramic, instrument, etc.)
# are kept constant.

from music import *
from random import *

# Define text to sonify.
# Excerpt from Herman Melville's "Moby-Dick", Epilogue (1851)

text = """The drama's done. Why then here does any one step forth? - Because one did survive the wreck. """

##### define the data structure
textMusicScore  = Score("Moby-Dick melody", 130)
textMusicPart   = Part("Moby-Dick melody", GLOCK, 0)
textMusicPhrase = Phrase()

# create durations list (factors correspond to probability)
durations = [HN] + [QN]*4 + [EN]*4 + [SN]*2

##### create musical data
for character in text:  # loop enough times

   value = ord(character)         # convert character to ASCII number

   # map printable ASCII values to a pitch value
   pitch = mapScale(value, 32, 126, C3, C6, PENTATONIC_SCALE, C2)

   # map printable ASCII values to a duration value
   index = mapValue(value, 32, 126, 0, len(durations)-1)
   duration = durations[index]

   print("value", value, "becomes pitch", pitch,)
   print("and duration", duration)

   dynamic = randint(60, 120)    # get a random dynamic

   note = Note(pitch, duration, dynamic)   # create note
   textMusicPhrase.addNote(note)  # and add it to phrase

# now, all characters have been converted to notes

# add ending note (same as last one - only longer)
note = Note(pitch, WN)
textMusicPhrase.addNote(note)

##### combine musical material
textMusicPart.addPhrase(textMusicPhrase)
textMusicScore.addPart(textMusicPart)

##### view score and write it to a MIDI file
View.show(textMusicScore)
Play.midi(textMusicScore)
Write.midi(textMusicScore, "textMusic.mid")