# arpeggiator2.py
#
# A basic arpeggiator using relative pitches.
#

from music import *

arpeggioPattern = [0, 4, 7, 12, 7, 4]   # arpeggiate a major chord
duration = TN                           # duration for each note

rootPitch   = eval(input("Enter root note (e.g., C4): "))
repetitions = eval(input("How many times to repeat arpeggio: "))

arpeggioPhrase = Phrase(0.0)        # phrase to store the arpeggio

# create arpeggiated sequence of notes
for interval in arpeggioPattern:
   pitch = rootPitch + interval # calculate absolute pitch
   n = Note(pitch, duration)    # create note with next pitch
   arpeggioPhrase.addNote(n)    # and add it to phrase

# now, the arpeggiation pattern has been created.

# repeat it as many times requested
Mod.repeat(arpeggioPhrase, repetitions)

# add final note to complete arpeggio
lastPitch = rootPitch + arpeggioPattern[0]  # close with first pitch
n = Note(lastPitch, duration * 4)   # but with longer duration
arpeggioPhrase.addNote(n)           # add it

Play.midi(arpeggioPhrase)