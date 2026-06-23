# audioLoopWithEnvelope.py
#
# Demonstrates how to create a loop using an audio file and an envelope.
# This may be used for ambient or drone backdrops of sound to build on.
#

from music import *

loopTimes = 4

# load audio instruments
a1 = AudioSample("moondog.Bird_sLament.wav")

# define an envelope
e1 = Envelope([20, 60, 100, 10], [0.0, 0.8, 1.0, 0.8], 30, 0.6, 30)
#e1 = Envelope()

# create musical data structure
score = Score()

part1 = Part(0, 0)

phrase1 = Phrase()

# create musical data
pitches   = [A4] * loopTimes
durations = [4.12152] * loopTimes   # duration is in seconds (assuming 60bpm)
volumes   = [120] * loopTimes
pannings  = [0.5] * loopTimes
lengths   =  durations              # force playing length to be same as noted duration!

phrase1.addNoteList(pitches, durations, volumes, pannings, lengths)

part1.addPhrase(phrase1)

score.addPart(part1)

# play it!
#Play.audio( score, [a1] )
Play.audio( score, [a1], [False], [e1] )
