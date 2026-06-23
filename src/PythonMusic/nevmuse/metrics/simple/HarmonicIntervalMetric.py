from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
import math

class HarmonicIntervalMetric(Metric):
   """
   It implements a Zipf metric capturing harmonic-interval proportion in a music piece.

   author Bill Manaris John Emerson, and Luca Pellicoro
   version 1.2 (February 26, 2007)
   version 1.1 (July 29, 2005)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a HarmonicIntervalMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("HarmonicInterval", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return HarmonicIntervalMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts all new harmonic intervals found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)   # holds the current time slice

      # count all new harmonic intervals within this time slice
      for i in range(len(timeSlice)):
         # if this is a new note and there is at least one more note with higher pitch...
         if timeSlice[i] > 0 and i + 1 < len(timeSlice):
            currentNote = pianoRoll.getNote(timeSlice[i])            # get the current note
            nextNote = pianoRoll.getNote(abs(timeSlice[i + 1]))      # get the next note
            interval = nextNote.getPitch() - currentNote.getPitch()  # calculate interval
            self.count(float(interval))                              # count it

         # if this a continuing note and there is at least one more note with higher pitch...
         if timeSlice[i] < 0 and i + 1 < len(timeSlice):  # if this note is a continuing note
            currentNote = pianoRoll.getNote(abs(timeSlice[i]))  # get the current note

            # count the harmonic interval only if the next note is new
            # (if the next note is a continuation, this interval has been counted already)
            if timeSlice[i + 1] > 0:
               nextNote = pianoRoll.getNote(timeSlice[i + 1])           # get the next note
               interval = nextNote.getPitch() - currentNote.getPitch()  # calculate interval
               self.count(float(interval))                              # count it
