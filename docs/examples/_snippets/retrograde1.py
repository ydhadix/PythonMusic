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

# now, create the retrograde phrase, and save it
pitches.reverse()  # reverse, using the reverse() list operation
rhythms.reverse()

retrograde = Phrase()
retrograde.addNoteList( pitches, rhythms )
Write.midi(retrograde, "retrogradeAfter.mid")