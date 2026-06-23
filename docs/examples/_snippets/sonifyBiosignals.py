# sonifyBiosignals.py
#
# Sonify skin conductance and heart data to pitch and dynamic.
#
# Sonification design:
#
# * Skin conductance is mapped to pitch (C3 - C6).
# * Heart value is mapped to a pitch variation (0 to 24).
# * Heart value is mapped to dynamic (0 - 127).
#
# NOTE: We quantize pitches to the C Major scale.
#

from music import *

# first let's read in the data
data = open("biosignals.txt", "r")

# read and process every line
skinData  = []     # holds skin data
heartData = []     # holds heart data
for line in data:

   time, skin, heart = line.split()  # extract the three values
   skin = float(skin)               # convert from string to float
   heart = float(heart)             # convert from string to float
   skinData.append(skin)            # keep the skin data
   heartData.append(heart)          # keep the heart data

# now, heartData contains all the heart values

data.close()    # done, so let's close the file

##### define the data structure
biomusicScore  = Score("Biosignal sonification", 150)
biomusicPart   = Part(PIANO, 0)
biomusicPhrase = Phrase()

# let's find the range extremes
heartMinValue = min(heartData)
heartMaxValue = max(heartData)
skinMinValue  = min(skinData)
skinMaxValue  = max(skinData)

# let's sonify the data
i = 0;   # point to first value in data
while i < len(heartData):   # while there are more values, loop

   # map skin-conductance to pitch
   pitch = mapScale(skinData[i], skinMinValue, skinMaxValue, C3, C6,
                    MAJOR_SCALE, C4)
   # map heart data to a variation of pitch
   pitchVariation = mapScale(heartData[i], heartMinValue,
                             heartMaxValue, 0, 24, MAJOR_SCALE, C4)

   # also map heart data to dynamic
   dynamic = mapValue(heartData[i], heartMinValue, heartMaxValue,
                      0, 127)

   # finally, combine pitch, pitch variation, and dynamic into note
   note = Note(pitch + pitchVariation, TN, dynamic)

   # add it to the melody so far
   biomusicPhrase.addNote(note)

   # point to next value in heart and skin data
   i = i + 1

# now, biomusicPhrase contains all the sonified values

##### combine musical material
biomusicPart.addPhrase(biomusicPhrase)
biomusicScore.addPart(biomusicPart)

##### view score and write it to a MIDI file
View.sketch(biomusicScore)
Write.midi(biomusicScore, "sonifyBiosignals.mid")
Play.midi(biomusicScore)