from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll

class ChordMetric(Metric):
   """
   It implements a Zipf metric capturing the proportion of chords in a music piece.

   author Bill Manaris and John Emerson and David Johnson
   version 1.5 (September 27, 2013)
   version 1.2 (February 26, 2007)
   version 1.0 (July 30, 2005)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a ChordMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("Chord", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return ChordMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts all new chords found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)      # get time slice

      # Algorithm:
      # Our goal is to identify and count new chords. Chords are any two or more notes that are playing
      # simultaneously.
      #
      # If there was at least one new note in this timeSlice (ie note index is positive), we create a chord identifier by arithetically
      # "concatenating" tones in a double value.  Since there are 128 MIDI values we multiple double by 128 after each interval added.
      # This results in a unique ID for all chord intervals

      isNewChord = False        # assume there are no new notes in this time slice

      # construct chord identifier (the idea is to spread tone values (1..127) throught the range of
      # a double value starting with the 10000th decimal position and increasing by a factor of 1000)
      place = 1.0   # initialize  UPDATE:  change to one; Test
      chordID = 0.0

      for i in range(len(timeSlice)):
         if timeSlice[i] > 0:  # if this is a new note (as opposed to a continuation)
            isNewChord = True    # so, we have a new chord

         note = pianoRoll.getNote(abs(timeSlice[i]))     # get the note (regardless if it's new or continuation)
         pitch = note.getPitch()                         # get the note's pitch

         # let's create the identifier even if not new so we only iterate over time slice once
         # we'll only add the chord to the count if it is a new one
         chordID += pitch * place     # concatenate this pitch value
         place *= 128                 # shift place by three decimal digits to the left

      # now, we have counted all tones in the time slice
      # and now, chordID contains every pitch sounding in the time slice, hence it can serve as a
      # unique, reproducable ID for this chord (but count it only if a new chord)
      if isNewChord:   # if this is a new chord...
         self.count(float(chordID))    # so, let's count it

   # Note: parallelBubbleSort and measureTimeSliceOld omitted as they appeared unused/deprecated in Java reference
