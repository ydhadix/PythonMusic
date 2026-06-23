# pianoPhaseWithBass.py
#
# Plays a variation on Steve Reich's minimalist piece, Piano Phase (1967).
# This variation adds a harmonic bass line derived from the main theme.
#

from music import *

pianoPart = Part(PIANO, 0) # create piano part

phrase1 = Phrase(0.0) # create three phrases
phrase2 = Phrase(0.0)
phrase3 = Phrase(0.0)

# write music in a convenient way
pitchList = [E4, FS4, B4, CS5, D5, FS4, E4, CS5, B4, FS4, D5, CS5]
durationList = [SN, SN, SN, SN, SN, SN, SN, SN, SN, SN, SN, SN]

# add the same notes to all three phrases
phrase1.addNoteList(pitchList, durationList)
phrase2.addNoteList(pitchList, durationList)
phrase3.addNoteList(pitchList, durationList)

# stretch phrase to play each bass note every 12 regular notes
Mod.elongate(phrase3, 12.0) # elongate (stretch) it 12 times

# transpose down two octaves (to create the harmonic bass line)
Mod.transpose(phrase3, -24)

Mod.repeat(phrase1, 48) # repeat first phrase
Mod.repeat(phrase2, 48) # repeat second phrase
Mod.repeat(phrase3, 48/12) # repeat elongated bass line - since it was
# stretched by 12 - to end at the same time

phrase1.setTempo(100.0) # set tempo to 100 beats-per-minute
phrase2.setTempo(100.5) # set tempo to 100.5 beats-per-minute
phrase3.setTempo(101.0) # set tempo to 101.0 beats-per-minute

pianoPart.addPhrase(phrase1) # add phrases to part
pianoPart.addPhrase(phrase2)
pianoPart.addPhrase(phrase3)

Play.midi(pianoPart) # and play it.