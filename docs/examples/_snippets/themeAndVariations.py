# themeAndVariations.py
#
# Demonstrates how to automatically develop musical material
# using a theme and transforming it through Mod functions.
#
# Here we start with the theme, continue with a few interesting
# variations, and close with the theme for recapitulation.

from music import *

# create theme
pitches = [C4, E4, G4, A4, B4, A4, B4, C5]
rhythms = [EN, EN, QN, SN, SN, SN, SN, QN]

theme = Phrase()
theme.addNoteList(pitches, rhythms)

# variation 1
# vary all pitches in theme, but keep the same
# rhythmic pattern (for stability)
var1 = theme.copy()    # preserve original (make a copy)
Mod.randomize(var1, 3) # randomize each pitch (max of +/- 3)
                       # (later we force them into the scale)
# variation 2
# slow down theme, and change two pitches using
# a random value from within the theme range
var2 = theme.copy()
Mod.elongate(var2, 2.0)  # double its time length
Mod.mutate(var2)         # change one pitch and rhythm value
Mod.mutate(var2)         # and another (could be the same)

# variation 3
# reverse the theme, and lower it one octave
var3 = theme.copy()
Mod.retrograde(var3)     # reverse notes
Mod.transpose(var3, -12) # lower one octave

# recapitulation
# repeat the theme for closing (i.e., return home)
var4 = theme.copy()      # we need a copy (a phrase can be added
                         # to a part only once)

# add theme and variations in the right order (since we
# didn't specify start times, they will play in sequence)
part = Part()
part.addPhrase(theme)
part.addPhrase(var1)
part.addPhrase(var2)
part.addPhrase(var3)
part.addPhrase(var4)

# now, fix all notes to be in the C major scale,
# and with rhythm values that line up with SN intervals
Mod.quantize(part, SN, MAJOR_SCALE, 0)

# provide alternate views
View.pianoRoll(part)
View.internal(part)
View.sketch(part)
Mod.consolidate(part)   # merge phrases into one phrase, so that...
View.notate(part)       # ...notate() can display all the notes

# and play
Play.midi(part)