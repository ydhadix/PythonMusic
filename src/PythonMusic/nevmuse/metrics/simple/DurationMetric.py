
from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics

class DurationMetric(Metric):
   """
   It implements a Zipf metric capturing note-duration proportion in a music piece.

   author John Emerson and Bill Manaris
   version 1.2 (February 26, 2007)
   version 1.1 (July 29, 2005)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a DurationMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level  the level of this metric (0 means base metric). Used internally by recursion.
      """
      super().__init__("Duration", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return DurationMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts the durations of all new notes found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)  # holds the current time slice

      # access all notes with current time slice
      for noteIndex in timeSlice:
         if noteIndex > 0:    # if this is a new note (as opposed to a continuation of an earlier note)
            note = pianoRoll.getNote(noteIndex) # get the note
            duration = note.getDuration()       # get this note's duration
            self.count(float(duration))         # and count it
