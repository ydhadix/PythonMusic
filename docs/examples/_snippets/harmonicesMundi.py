# harmonicesMundi.py
#
# Sonify mean planetary velocities in the solar system.
#

from music import *

# create a list of planet mean orbital velocities
# Mercury, Venus, Earth, Mars, Ceres, Jupiter,
#  Saturn, Uranus, Neptune, Pluto
planetVelocities = [47.89, 35.03, 29.79, 24.13, 17.882, 13.06,
                     9.64, 6.81, 5.43, 4.74]

# get minimum and maximum velocities:
minVelocity = min(planetVelocities)
maxVelocity = max(planetVelocities)

# calculate pitches
planetPitches   = []    # holds list of sonified velocities
planetDurations = []    # holds list of durations
for velocity in planetVelocities:
   # map a velocity to pitch and save it
   pitch = mapScale(velocity, minVelocity, maxVelocity, C1, C6,
                    CHROMATIC_SCALE)
   planetPitches.append( pitch )
   planetDurations.append( EN )   # for now, keep duration fixed

# create the planet melodies
melody1 = Phrase(0.0)      # starts at beginning
melody2 = Phrase(10.0)     # starts 10 beats into the piece
melody3 = Phrase(20.0)     # starts 20 beats into the piece

# create melody 1 (theme)
melody1.addNoteList(planetPitches, planetDurations)

# melody 2 starts 10 beats into the piece and
# is elongated by a factor of 2
melody2 = melody1.copy()
melody2.setStartTime(10.0)
Mod.elongate(melody2, 2.0)

# melody 3 starts 20 beats into the piece and
# is elongated by a factor of 4
melody3 = melody1.copy()
melody3.setStartTime(20.0)
Mod.elongate(melody3, 4.0)

# repeat melodies appropriate times, so they will end together
Mod.repeat(melody1, 8)
Mod.repeat(melody2, 3)

# create parts with different instruments and add melodies
part1 = Part("Eighth Notes", PIANO, 0)
part2 = Part("Quarter Notes", FLUTE, 1)
part3 = Part("Half Notes", TRUMPET, 3)
part1.addPhrase(melody1)
part2.addPhrase(melody2)
part3.addPhrase(melody3)

# finally, create, view, and write the score
score = Score("Celestial Canon")
score.addPart(part1)
score.addPart(part2)
score.addPart(part3)
View.sketch(score)
Play.midi(score)
Write.midi(score, "harmonicesMundi.mid")