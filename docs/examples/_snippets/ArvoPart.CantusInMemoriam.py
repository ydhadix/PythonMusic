# ArvoPart.CantusInMemoriam.py
#
# Recreates a variation of Arvo Part's "Cantus in Memoriam Benjamin
# Britten" (1977) for string orchestra and bell, using Mod functions.

from music import *

# musical parameters
repetitions = 2   # length of piece
tempo = 112       # tempo of piece
bar = WN+HN       # length of a measure

# create musical data structure
cantusScore = Score("Cantus in Memoriam Benjamin Britten", tempo)

bellPart = Part(TUBULAR_BELLS, 0)
violinPart = Part(VIOLIN, 1)

# bell
bellPitches   = [REST,  A4,    REST, REST,  A4,    REST, REST,  A4]
bellDurations = [bar/2, bar/2, bar,  bar/2, bar/2, bar,  bar/2, bar/2]

bellPhrase = Phrase(0.0)
bellPhrase.addNoteList(bellPitches, bellDurations)
bellPart.addPhrase(bellPhrase)

# violin - define descending aeolian scale and rhythms
pitches   = [A5, G5, F5,  E5,  D5,  C5,  B4,  A4]
durations = [HN, QN, HN, QN, HN, QN, HN, QN]

# violin 1
violin1Phrase = Phrase(bar * 6.5)  # start after 6 and 1/2 measures
violin1Phrase.addNoteList(pitches, durations)

# violin 2
violin2Phrase = violin1Phrase.copy()
violin2Phrase.setStartTime(bar * 7.0)  # start after 7 measures
Mod.elongate(violin2Phrase, 2.0)       # double durations
Mod.transpose(violin2Phrase, -12)      # an octave lower

# violin 3
violin3Phrase = violin2Phrase.copy()
violin3Phrase.setStartTime(bar * 8.0)  # start after 8 measures
Mod.elongate(violin3Phrase, 2.0)       # double durations
Mod.transpose(violin3Phrase, -12)      # an octave lower

# violin 4
violin4Phrase = violin3Phrase.copy()
violin4Phrase.setStartTime(bar * 10.0) # start after 10 measures
Mod.elongate(violin4Phrase, 2.0)       # double durations
Mod.transpose(violin4Phrase, -12)      # an octave lower

# repeat phrases enough times
Mod.repeat(violin1Phrase, 8 * repetitions)
Mod.repeat(violin2Phrase, 4 * repetitions)
Mod.repeat(violin3Phrase, 2 * repetitions)
Mod.repeat(violin4Phrase, repetitions)

# violin part
violinPart.addPhrase(violin1Phrase)
violinPart.addPhrase(violin2Phrase)
violinPart.addPhrase(violin3Phrase)
violinPart.addPhrase(violin4Phrase)

# score
cantusScore.addPart(bellPart)
cantusScore.addPart(violinPart)

# fade in, and fade out
Mod.fadeIn(cantusScore, WN)
Mod.fadeOut(cantusScore, WN * 12)

# view, play, and write
View.sketch(cantusScore)
Play.midi(cantusScore)
Write.midi (cantusScore, "ArvoPart.CantusInMemoriam.mid")