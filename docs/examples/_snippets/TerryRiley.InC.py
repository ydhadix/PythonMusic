# TerryRiley.InC.py
#
# Live coding performance of Terry Riley's "In C".
# See http://www.flagmusic.com/content/clips/inc.pdf

from music import *
from timer import *

# redefine these notes at will
pitches   = [E4, F4, E4]
durations = [SN, SN, EN]

# play above pitches and durations in a continuous loop
def loopMusic():

   global pitches, durations

   # create phrase from current pitches and durations
   theme = Phrase()
   theme.addNoteList( pitches, durations )

   # play it
   Play.midi( theme )

   # get duration of phrase in millisecs (assume 60BPM)
   duration = int( theme.getBeatLength() * 1000 )

   # create and start timer to call this function
   # once recursively, after the elapsed duration
   t = Timer( duration, loopMusic, [], False )
   t.start()

# start playing
loopMusic()