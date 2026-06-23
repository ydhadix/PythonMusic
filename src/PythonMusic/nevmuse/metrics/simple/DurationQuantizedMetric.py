from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll

class DurationQuantizedMetric(Metric):
   """
   It implements a Zipf metric capturing quantized note-duration proportion in a music piece.  The quantization depends
   on the PianoRoll quantum.

   author Bill Manaris
   version 1.0 (January 7, 2010)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a DurationQuantizedMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("DurationQuantized", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return DurationQuantizedMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts the quantized durations of all new notes found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)  # holds the current time slice

      # access all notes with current time slice
      for i in range(len(timeSlice)):
         if timeSlice[i] > 0:    # if this is a new note (as opposed to a continuation of an earlier note)
            note = pianoRoll.getNote(timeSlice[i])           # get the note
            quantizedDuration = note.getDurationQuantized()  # get this note's quantized duration
            self.count(float(quantizedDuration))             # and count it
