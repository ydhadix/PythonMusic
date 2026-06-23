from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll

class DurationDistanceMetric(Metric):
   """
   It implements a Zipf metric capturing proportion of distances between notes with same duration.

   author Brys Sepulveda and Bill Manaris
   version 1.0 (September 26, 2009)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a DurationDistanceMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("DurationDistance", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return DurationDistanceMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      Counts all distances between the first occurance of a new duration (found in the specified time slice of the piano roll)
      and the next occurence of the same duration.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)   # holds the current time slice

      for i in range(len(timeSlice)):
         if timeSlice[i] > 0:  # if this is a new note (as opposed a continuation of an earlier note)
            currentNote = pianoRoll.getNote(timeSlice[i])        # get it
            currentNoteDuration = currentNote.getDuration()      # get its duration

            # get the next note with same duration (if any)
            futureNote = pianoRoll.getNextNoteSameDuration(currentNoteDuration, timeIndex)

            if futureNote is not None:   # if there is a future note with the same duration as currentNote
               # calculate the distance between the two notes -- for consistency, we measure distance from
               # the beginning of notes (so distances are not sensitive to note duration).
               distance = futureNote.getStartTime() - currentNote.getStartTime()              # get distance
               self.count(float(distance))                                                    # and count it
