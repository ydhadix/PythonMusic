from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll

class ContourMelodyPitchMetric(Metric):
   """
   It implements a Zipf metric capturing pitch proportion of the highest voice (melody contour) in a music piece.
   For simplicity, it assumes the highest voice sings the highest note in a timeslice.

   author Bill Manaris
   version 1.0 (January 7, 2010)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a ContourMelodyPitchMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("ContourMelodyPitch", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return ContourMelodyPitchMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts the highest pitch found in the specified time slice of the piano roll,
      but *only* if it belongs to a new note.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)  # holds the current time slice

      # get the highest note in the current timeslice and, if new, count it
      # (assume that the highest note is at the end (top) of the timeslice
      if len(timeSlice) > 0:   # is there a note?
         if timeSlice[-1] > 0:   # is this a new note (as opposed to a continuation of an earlier note)
            note = pianoRoll.getNote(timeSlice[-1])     # get the note
            pitch = note.getPitch()                     # get this note's pitch
            self.count(float(pitch))                    # capture the change in proportion introduced by this pitch
