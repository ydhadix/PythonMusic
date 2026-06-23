from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll

class ChromaticToneMetric(Metric):
   """
   It implements a Zipf metric capturing chromatic tone (pitch mod 12) proportion in a music piece.

   author Bill Manaris and Luca Pellicoro
   version 1.2 (February 26, 2007)
   version 1.1 (July 29, 2005)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a ChromaticToneMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("ChromaticTone", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return ChromaticToneMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts all new chromatic tones found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)  # holds the current time slice

      # access all notes with current time slice and increment the corresponding pitch count
      for i in range(len(timeSlice)):
         if timeSlice[i] > 0:    # if this is a new note (as opposed to a continuation of an earlier note)
            note = pianoRoll.getNote(timeSlice[i])   # get the note
            pitch = note.getPitch()                  # get this note's pitch
            self.count(float(pitch % 12))            # increment count for this chromatic tone
