from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll

class ContourBasslineDurationMetric(Metric):
   """
   It implements a Zipf metric capturing duration proportion of the lowest voice (bassline contour) in a music piece.
   For simplicity, it assumes the bassline consists of all the lowest notes in the piano roll.

   author Bill Manaris
   version 1.0 (January 7, 2010)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a ContourBasslineDurationMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("ContourBasslineDuration", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return ContourBasslineDurationMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts the duration of the lowest pitch found in the specified time slice of the piano roll,
      but *only* if it belongs to a new note.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)  # holds the current time slice

      # get the lowest note in the current timeslice and, if new, count it
      # (assume that the lowest note is at the beginning (bottom) of the timeslice
      if len(timeSlice) > 0:   # is there a note?
         if timeSlice[0] > 0:        # is this a new note (as opposed to a continuation of an earlier note)
            note = pianoRoll.getNote(timeSlice[0])       # get the note
            duration = note.getDuration()                # get this note's duration
            self.count(float(duration))                  # capture the change in proportion introduced by this duration
