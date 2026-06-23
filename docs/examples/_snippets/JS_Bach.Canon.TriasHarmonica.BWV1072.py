# JS_Bach.Canon.TriasHarmonica.BWV1072.py
#
# This program creates J.S. Bach's 'Trias Harmonica' BWV 1072 canon.
#
# This canon is constructed using two parts (choirs), each consisting
# of four voices. The first part's voices use the original theme,
# each separated by a half-note delay. The second part's voices use
# the inverted theme delayed by a quarter note, each separated by
# a half-note delay.
#

from music import *

# define the theme (for choir 1)
pitches1   = [C4,  D4, E4,  F4, G4,  F4, E4,  D4]
durations1 = [DQN, EN, DQN, EN, DQN, EN, DQN, EN]

# define the inverted theme (for choir 2)
pitches2   = [G4,  F4, E4,  D4, C4,  D4, E4,  F4]
durations2 = [DQN, EN, DQN, EN, DQN, EN, DQN, EN]

# how many times to repeat the theme
times = 8

# choir 1 - 4 voices separated by half note
choir1 = Part()

voice1 = Phrase(0.0)
voice1.addNoteList(pitches1, durations1)
Mod.repeat(voice1, times)           # repeat a number of times
voice1.addNote(C4, DQN)             # add final note

voice2 = voice1.copy()              # voice 2 is a copy of voice 1
voice2.setStartTime(HN)             # separated by half note

voice3 = voice1.copy()              # voice 3 is a copy of voice 1
voice3.setStartTime(HN*2)           # separated by two half notes

voice4 = voice1.copy()              # voice 4 is a copy of voice 1
voice4.setStartTime(HN*3)           # separated by three half notes

choir1.addPhrase(voice1)
choir1.addPhrase(voice2)
choir1.addPhrase(voice3)
choir1.addPhrase(voice4)

# choir 2 - 4 voices inverted, delayed by quarter note,
# separated by a half note.
choir2 = Part()

voice5 = Phrase(QN)                 # delayed by quarter note
voice5.addNoteList(pitches2, durations2)
Mod.repeat(voice5, times)           # repeat a number of times
voice5.addNote(G4, DQN)             # add final note

voice6 = voice5.copy()              # voice 6 is a copy of voice 5
voice6.setStartTime(QN + HN)        # separated by half note

voice7 = voice5.copy()              # voice 7 is a copy of voice 5
voice7.setStartTime(QN + HN*2)      # separated by two half notes

voice8 = voice5.copy()              # voice 8 is a copy of voice 5
voice8.setStartTime(QN + HN*3)      # separated by three half note

choir2.addPhrase(voice5)
choir2.addPhrase(voice6)
choir2.addPhrase(voice7)
choir2.addPhrase(voice8)

# score
canon = Score("J.S. Bach, Trias Harmonica (BWV 1072)", 100)
canon.addPart(choir1)
canon.addPart(choir2)

# play score, and write it to a MIDI file
Play.midi(canon)
Write.midi(canon, "JS_Bach.Canon.TriasHarmonica.BWV1072.mid")