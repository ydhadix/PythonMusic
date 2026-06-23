# proteinMusic.py
#
# Demonstrates how to utilize list operations to build an unfolding piece
# of music based on the first 13 amino acids in the human thymidylate
# synthase A (ThyA) protein.
#
# The piece starts with the 1st amino acid, continues with the 1st and 2nd
# amino acids, then with the 1st, 2nd, and 3rd amino acids, and so on,
# until all 13 amino acids have been included.
#
# See: Takahashi, R. and Miller, J.H. (2007), "Conversion of Amino-Acid
# Sequence in Proteins to Classical Music: Search for Auditory Patterns",
# Genome Biology, 8(5), p. 405.

from music import *

# set of pitches/rhythms to use for building incremental piece
pitches = [[D3, F3, A3], [E3, G3, B3], [B3, D4, F4], [D4, F4, B4],
            [D4, F4, A4], [G4, B4, E5], [G4, B4, D5], [A4, C4, E4],
             [B3, G3, E3], [A4, C5, E5], [A4, C5, E5], [E3, G3, B3],
              [A3, C4, E4]]
rhythms = [HN,           QN,           HN,           QN,
            HN,           EN,           WN,           WN,
             EN,           QN,           QN,           QN,
              QN]

# we will store each incremental portion in a separate phrase
phraseList = []   # holds incremental phrases

# iterate through every index of the pitch/rhythm set
for i in range( len(pitches) ):

   # get next incremental slice of pitches/rhythms
   growingPitches = pitches[0:i+1]
   growingRhythms = rhythms[0:i+1]

   # build next incremental phrase (no start time - for sequential play)
   phrase = Phrase()            # create empty phrase
   phrase.addNoteList( growingPitches, growingRhythms)
   silenceGap = Note(REST, HN)  # add a separator at the end of the phrase...
   phrase.addNote( silenceGap ) # ...to distinguish from subsequent phrases

   # remember this phrase
   phraseList.append( phrase )

# now, phraseList contains incremental phrases from set of pitches/rhythms

# add incremental phrases to a part
part = Part()
for phrase in phraseList:
   part.addPhrase( phrase )
# now, all phrases have been added to the part

# set the tempo
part.setTempo(220)

# view part and play
View.sketch( part )
Play.midi( part )