# retrograde.py
#
# Demonstrates one way to reverse the notes in a phrase.
#

from music import *

# create a phrase, add some notes to it, and save it (for comparison)
pitches = [C4, D4, E4, F4, G4, A4, B4,   C5]    # the C major scale
rhythms = [WN, HN, QN, EN, SN, TN, TN/2, TN/4]  # increasing tempo

phrase = Phrase()
phrase.addNoteList( pitches, rhythms )
Write.midi(phrase, "retrogradeBefore.mid")

### now, a more economical way...

# get the notes from the phrase
noteList = phrase.getNoteList()   # this gives us a list

pitches   = []  # create empty lists of pitches
durations = []  # ...and durations

# iterate *backwards* through every note in the note list
numNotes = len( noteList )   # get the number of notes in the list

# iterate through all the notes in reverse order
for i in range( numNotes ):

   # calculate index from the other end of the list
   reverseIndex = numNotes - i - 1

   note = noteList[reverseIndex]   # get corresponding note

   pitches.append( note.getPitch() )      # append this pitch
   durations.append( note.getDuration() ) # append this duration

# now, create the retrograde phrase, and save it
retrograde = Phrase()
retrograde.addNoteList( pitches, durations )
Write.midi(retrograde, "retrogradeAfter.mid")