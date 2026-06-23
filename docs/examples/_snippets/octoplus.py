# octoplus.py
#
# A music effect based loosely on the DOD FX-35 guitar pedal.
# It takes a music phrase and generates another phrase containing
# the original notes plus an octave lower, and a fifth lower.

from music import *

# program constants
instrument = STEEL_GUITAR
tempo = 110

# test melody - riff from Deep Purple's "Smoke on the Water"
pitches = [G2, AS2, C3,  G2, AS2, CS3, C3, G2, AS2, C3,  AS2, G2]
durs    = [QN, QN,  DQN, QN, QN,  EN,  HN, QN, QN,  DQN, QN,  DHN+EN]

#################
# create original melody
originalPhrase = Phrase()

# set parameters
originalPhrase.setInstrument( instrument )
originalPhrase.setTempo( tempo )

originalPhrase.addNoteList(pitches, durs)

#################
# create effect melody (original + octave lower + fifth lower)
octoplusPhrase = Phrase()

# set parameters
octoplusPhrase.setInstrument( instrument )
octoplusPhrase.setTempo( tempo )

# for every note in original, create effect notes
for note in originalPhrase.getNoteList():

   pitch = note.getPitch()        # get this note's pitch
   duration = note.getDuration()  # and duration

   # build list of effect pitches, for given note
   chordPitches = []                  # create list to store pitches
   chordPitches.append( pitch )       # add original pitch
   chordPitches.append( pitch - 12 )  # add octave below
   chordPitches.append( pitch - 5 )   # add fifth below
   # now, list of concurrent pitches if ready, so...

   # add effect pitches (a chord) and associated duration to phrase
   octoplusPhrase.addChord( chordPitches, duration )

# now, we have looped through all pitches, and effect phrase is built

#################
# save both versions (for comparison purposes)
Write.midi(originalPhrase, "octoplusOriginal.mid")
Write.midi(octoplusPhrase, "octoplusEffect.mid")