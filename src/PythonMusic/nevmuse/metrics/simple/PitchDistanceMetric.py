from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll

class PitchDistanceMetric(Metric):
   """
   It implements a Zipf metric capturing proportion of distances between identical pitches in a music piece.

   author John Emerson, and Bill Manaris
   version 1.2 (February 26, 2007)
   version 1.0 (July 29, 2005)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a PitchDistanceMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("PitchDistance", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return PitchDistanceMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts all distances between the first occurance of a new pitch (found in the specified time slice of the piano roll)
      and the next occurence of the same pitch.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)   # holds the current time slice

      # access all the notes with current time slice
      for i in range(len(timeSlice)):
         if timeSlice[i] > 0:  # if this is a new note (as opposed a continuation of an earlier note)
            currentNote = pianoRoll.getNote(timeSlice[i])  # get it
            currentNotesPitch = currentNote.getPitch()     # get it's pitch

            # get the next note with same pitch (if any)
            futureNote = pianoRoll.getNextNoteSamePitch(currentNotesPitch, timeIndex)

            if futureNote is not None:   # if there is a future note with the same pitch as currentNote
               # calculate the distance between the two notes
               currentNoteEndTime = currentNote.getStartTime() + currentNote.getDuration() # get end time of current note
               distance = futureNote.getStartTime() - currentNoteEndTime                      # get distance
               self.count(float(distance))                                                    # and count it
