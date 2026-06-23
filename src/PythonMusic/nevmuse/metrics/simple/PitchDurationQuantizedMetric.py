from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll

class PitchDurationQuantizedMetric(Metric):
   """
   It implements a Zipf metric capturing pitch-duration proportion in a music piece.

   author Bill Manaris
   version 1.0 (January 7, 2010)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a PitchDurationQuantizedMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("PitchDurationQuantized", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return PitchDurationQuantizedMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts all new quantized pitch-durations found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)  # holds the current time slice

      # access all notes with current time slice and increment the corresponding count for this quantized pitch&duration
      for i in range(len(timeSlice)):
         if timeSlice[i] > 0:    # if this is a new note (as opposed to a continuation of an earlier note)
            note = pianoRoll.getNote(timeSlice[i])                    # get the note

            # Let's combine the pitch of a note and its quantized duration into one value.
            # In particular, pitch is stored in the integral part of the double value,
            # whereas quantized duration is stored in the decimal part.
            # This produces a unique value for each quantized pitch-duration combination.
            # Calculating the difference of two such values (i.e., higher-order metrics),
            # still produces a meaningful value (where the integral part is the difference of the two pitches,
            # and the decimal part is the difference of the quantized durations.
            key = (note.getPitch()) + (note.getDurationQuantized() / 100.0)

            self.count(float(key))     # increment count for this pitch&duration combination
