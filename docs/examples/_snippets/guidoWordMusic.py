# guidoWordMusic.py
#
# Creates a melody from text using the following rules:
#
# 1) Vowels specify pentatonic pitch, 'a' is C4, 'e' is D4,
#    'i' is E4, 'o' is G4, and 'u' is A4.
#
# 2) Consonants are ignored, but contribute to note duration of
#    all vowels within a word (if any).
#

from music import *

# this is the text to be sonified
text = """One of the oldest known algorithmic music processes is a rule-based algorithm that selects each note based on the letters in a text, credited to Guido d'Arezzo."""

text = text.lower()   # convert string to lowercase

# define vowels and corresponding pitches (parallel sequences),
# i.e., first vowel goes with first pitch, and so on.
vowels       = "aeiou"
vowelPitches = [C4, D4, E4, G4, A4]

# define consonants
consonants = "bcdfghjklmnpqrstvwxyz"

# define parallel lists to hold pitches and durations
pitches   = []
durations = []

# factor used to scale durations
durationFactor = 0.1   # higher for longer durations

# separate text into words (using space as delimiter)
words = text.split()

# iterate through every word in the text
for word in words:

   # iterate through every character in this word
   for character in word:

      # is this character a vowel?
      if character in vowels:

         # yes, so find its position in the vowel list
         index = vowels.find(character)

         # and use position to find the corresponding pitch
         pitch = vowelPitches[index]

         # finally, remember this pitch
         pitches.append( pitch )

         # create duration from the word length
         duration = len( word ) * durationFactor

         # and remember it
         durations.append( duration )

# now, pitches and durations have been created

# so, add them to a phrase
melody = Phrase()
melody.addNoteList(pitches, durations)

# view and play melody
View.notation(melody)
Play.midi(melody)