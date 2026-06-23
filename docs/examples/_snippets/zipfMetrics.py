# zipfMetrics.py
#
# Demonstrates how to calculate Zipf metrics from MIDI files for
# comparative analysis. It calculates Zipf slopes and R^2 values
# for pitch.
#
# It also demonstrates how to use Python dictionaries to store
# collections of related items.
#
# Finally, it demonstrates how to implement an algorithm in a top-down
# fashion. First function encountered in the program performs the
# highest-level tasks, and any sub-tasks are relegated to lower-level
# functions.
#

from music import *
from zipf import *

# list of MIDI files to analyze
pieces = ["sonifyBiosignals.mid", "ArvoPart.CantusInMemoriam.mid",
          "DeepPurple.SmokeOnTheWater.mid",
          "soundscapeLoutrakiSunset.mid",
          "Pierre Cage.Structures pour deux chances.mid"]

# define main function
def main( pieces ):
   """Calculates and outputs Zipf statistics of all 'pieces'."""

   # read MIDI files and count pitches
   for piece in pieces:

      # read this MIDI file into a score
      score = Score() # create an empty score
      Read.midi( score, piece ) # and read MIDI file into it

      # count the score's pitches
      histogram = countPitches( score )

      # calculate Zipf slope and R^2 value
      counts = histogram.values()
      slope, r2, yint = byRank(counts)

      # output results
      print("Zipf slope is", round(slope, 4), ", R^2 is", round(r2, 2),)
      print("for", piece)
      print()

   # now, all the MIDI files have been read into dictionary
   print() # output one more newline

def countPitches( score ):
   """Returns count of how many times each individual pitch appears
   in 'score'.
   """

   histogram = {} # holds each of the pitches found and its count

   # iterate through every part, and for every part through every
   # phrase, and for every phrase through every note (via nested
   # loops)
   for part in score.getPartList(): # for every part
      for phrase in part.getPhraseList(): # for every phrase in part
         for note in phrase.getNoteList(): # for every note in phrase

            pitch = note.getPitch() # get this note's pitch

            # count this pitch, if not a rest
            if (pitch != REST):

               # increment this pitch's count (or initialize to 1)
               histogram[ pitch ] = histogram.get(pitch, 0) + 1

         # now, all the notes in this phrase have been counted
      # now, all the phrases in this part have been counted
   # now, all the parts have been counted

   # done, so return counts
   return histogram

# start the program
main( pieces )