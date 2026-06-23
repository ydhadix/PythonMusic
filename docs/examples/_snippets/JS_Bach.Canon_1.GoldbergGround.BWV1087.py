# JS_Bach.Canon_1.GoldbergGround.BWV1087.py
#
# This program (re)creates J.S. Bach's Canon No. 1 of the Fourteen on
# the Goldberg Ground.
#
# This canon is constructed using the Goldberg ground as the subject
# (soggetto) combined with the retrograde of itself.
#

from music import *

# how many times to repeat the theme
times = 6

# define the data structure
score  = Score("J.S. Bach, Canon 1, Goldberg Ground (BWV1087)", 100)
part   = Part()
voice1 = Phrase(0.0)

# create musical material (soggetto)
pitches = [G3, F3, E3, D3, B2, C3, D3, G2]
rhythms = [QN, QN, QN, QN, QN, QN, QN, QN]
voice1.addNoteList(pitches, rhythms)

# create 2nd voice
voice2 = voice1.copy()
Mod.retrograde(voice2)   # follower is retrograde of leader

# combine musical material
part.addPhrase(voice1)
part.addPhrase(voice2)
score.addPart(part)

# repeat canon as desired
Mod.repeat(score, times)

# play score and write it to a MIDI file
Play.midi(score)
Write.midi(score, "JS_Bach.Canon_1.GoldbergGround.BWV1087.mid")