from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
import math

class HarmonicBigramMetric(Metric):
   """
   It implements a Zipf metric capturing proportion of harmonic-bigrams in a music piece.

   author John Emerson and Bill Manaris
   version 1.2 (February 26, 2007)
   version 1.1 (Aug 1, 2005)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a HarmonicBigramMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("HarmonicBigram", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return HarmonicBigramMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts all new harmonic-bigrams found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)   # holds the current time slice

      # access all notes with current time slice, identify each harmonic bigram, and count it
      # (Note: Since we always need a next harmonic note in order to create a bigram with,
      #  the last we go into the loop is when 'i' is pointing to the penultimate note in the time slice.)
      for i in range(len(timeSlice) - 1):

         # if this note is a new note
         if timeSlice[i] > 0:
            currentNote = pianoRoll.getNote(timeSlice[i])             # get the current note
            nextNote = pianoRoll.getNote(abs(timeSlice[i + 1]))       # get the next note (regardless if it's new or continuation)

            # Let's combine the pitches of the two notes into one value.
            # ... (comment preserved from Java) ...
            # (Note: since pitch may range from 0..127, we divide by 1000 to ensure that the
            #  second pitch ends up well into the decimal part.)
            harmonicBigram = currentNote.getPitch() + (nextNote.getPitch() / 1000.0)   # assmeble harmonic bigram indentifier
            self.count(harmonicBigram)                                                 # and count it

         # if this note is a continuation, and the next note is new
         if timeSlice[i] < 0 and timeSlice[i + 1] > 0:
            currentNote = pianoRoll.getNote(abs(timeSlice[i]))        # get the current note
            nextNote = pianoRoll.getNote(abs(timeSlice[i + 1]))       # get the next note (regardless if it's new or continuation)

            # ... (comment preserved) ...
            harmonicBigram = currentNote.getPitch() + (nextNote.getPitch() / 1000.0)   # assmeble harmonic bigram indentifier
            self.count(harmonicBigram)                                                 # and count it
