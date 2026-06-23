from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics

class MelodicIntervalMetric(Metric):
   """
   It implements a Zipf metric capturing the proportion of melodic intervals in a music piece.

   author Hector Mojica, and Bill Manaris
   version 1.2 (February 26, 2007)
   version 1.1 (July 29, 2005)
   version 1.0 (June 13, 2005)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a MelodicIntervalMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("MelodicInterval", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return MelodicIntervalMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts all new melodic intervals found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)  # holds the current time slice

      # access all notes with current time slice and increment the count
      for i in range(len(timeSlice)):
         if timeSlice[i] > 0:  # if this is a new note (as opposed to a continuation of an earlier note)
            note = pianoRoll.getNote(timeSlice[i])       # get the note
            pitch = note.getPitch()                      # get this note's pitch
            voice = note.getVoice()                      # get this note's voice
            nextNote = pianoRoll.getNextNoteSameVoice(voice, timeIndex) # get the next note that matches current note's voice

            if nextNote is not None:  # check if there even is a next note
               # increment count
               # Note: super.count() in Java takes Double. Python handles types automatically.
               self.count(float(pitch - nextNote.getPitch()))
