# arpeggiator1.py
#
# A basic arpeggiator using absolute pitches.
#

from music import *

arpeggioPattern = [C4, E4, G4, C5, G4, E4]   # arpeggiate the C chord
duration = TN                                # duration for each note

repetitions = eval(input("How many times to repeat arpeggio: "))

arpeggioPhrase = Phrase(0.0)        # phrase to store the arpeggio

# create arpeggiated sequence of notes
for pitch in arpeggioPattern:
   n = Note(pitch, duration)    # create note with next pitch
   arpeggioPhrase.addNote(n)    # and add it to phrase

# now, the arpeggiation pattern has been created.

# repeat it as many times requested
Mod.repeat(arpeggioPhrase, repetitions)

# add final note to complete arpeggio
lastPitch = arpeggioPattern[0]      # use first pitch as last pitch
n = Note(lastPitch, duration * 2)   # using longer duration
arpeggioPhrase.addNote(n)           # add it

Play.midi(arpeggioPhrase)