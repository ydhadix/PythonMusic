# pianoRollGenerator.py
#
# Task:   An interactive pianoRoll generator.
#
# Input:  User selects MIDI instrument and enters pitches
#         one at a time.
#
# Output: Program generates a pianoRoll for the entered pitches,
#         and plays the corresponding notes.
#
# Limitation: Currently, all notes have QN durations.

from music import *

# ask user to select a MIDI instrument
instrument = eval(input("Select MIDI instrument (0-127): "))

# output the name of the selected instrument
print("You picked", MIDI_INSTRUMENTS[instrument])

howMany = eval(input("How many notes to play (0 or more): "))

pitches = []   # to be populated via user input

for i in range(howMany):                 # loop this many times
   pitch = eval(input("Enter note (e.g., C4): ")) # get next pitch
   pitches.append( pitch )                  # append to pitch list

# now, all pitches have been entered by user and stored in pitches

# create notes
phrase = Phrase()                        # create empty phrase
phrase.setInstrument( instrument )       # use selected instrument

for pitch in pitches:                    # for each pitch in the list
   note = Note( pitch, QN )                 # create next note
   phrase.addNote( note )                   # and add it to phrase

# now, all notes have been created and stored in phrase

# generate pianoRoll and play notes
View.pianoRoll( phrase )
Play.midi( phrase )