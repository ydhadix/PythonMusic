# scaleTutor.py
#
# Outputs the pitches of a scale, starting at a given root.
#
# Also demonstrates the reverse look-up of MIDI constants using music
# library's MIDI_PITCHES list.

from music import *

print("This program outputs the pitches of a scale.")

# get which scale they want
scale = eval(input("Enter scale (e.g., MAJOR_SCALE): "))

# get root pitch
root = eval(input("Enter root note (e.g., C4): "))

# output the pitches in this scale
print("The notes in this scale are",)   # print prefix (no newline)

# iterate through every interval in the chosen scale
for interval in scale:
   pitch = root + interval     # add interval to root
   print(MIDI_PITCHES[pitch],)  # print pitch name (no newline)

# after the loop
print(".")  # done, so output newline