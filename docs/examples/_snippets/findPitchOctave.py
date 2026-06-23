# findPitchOctave.py
# Given a MIDI pitch integer, find its octave.

from music import *        # import music library

# get input from user
pitch = eval(input("Please enter a MIDI pitch (0 - 127): "))

# an octave has 12 pitches, and octave numbering starts at -1, so
# division by 12 and subtracting 1 gives us the octave (e.g. 4th)
octave = (pitch / 12) - 1

# output result
print("MIDI pitch", pitch, "is in octave", octave)