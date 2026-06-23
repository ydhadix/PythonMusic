from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll
import math

class ChordDistanceMetric(Metric):
   """
   It implements a Zipf metric capturing proportion of distances between identical pitches in a music piece.

   author John Emerson, and Bill Manaris
   version 1.2 (February 26, 2007)
   version 1.0 (July 29, 2005)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a ChordDistanceMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("ChordDistance", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return ChordDistanceMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts all distances between the first occurance of a new pitch (found in the specified time slice of the piano roll)
      and the next occurence of the same pitch.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)   # holds the current time slice
      found = False

      if self.isNewChord(timeSlice):
         currentPitchList = self.createPitchList(timeSlice, pianoRoll)

         searchIndex = timeIndex + 1
         while searchIndex < pianoRoll.getLength() and not found:
            futureTimeSlice = pianoRoll.getTimeSlice(searchIndex)

            if self.isNewChord(futureTimeSlice):
               futurePitchList = self.createPitchList(futureTimeSlice, pianoRoll)

               if currentPitchList == futurePitchList:
                  found = True
                  distance = self.calculateChordDistance(timeSlice, futureTimeSlice, pianoRoll)
                  self.count(float(distance))

            searchIndex += 1

   def isNewChord(self, timeSlice):
      """
      Checks if any note in the time slice is new (positive index).
      """
      for s in timeSlice:
         if s > 0:
            return True
      return False

   def createPitchList(self, timeSlice, pianoRoll):
      """
      Creates a list of pitches for the notes in the time slice.
      """
      pitchList = []
      for s in timeSlice:
         pitchList.append(pianoRoll.getNote(abs(s)).getPitch())
      return pitchList

   def calculateChordDistance(self, timeSlice, futureTimeSlice, pianoRoll):
      """
      Calculates distance between the end of the current chord and the start of the next identical chord.
      """
      # may need to update to use Note with shortest length...
      currentNote = pianoRoll.getNote(abs(timeSlice[0]))
      futureNote = pianoRoll.getNote(abs(futureTimeSlice[0]))

      currentNoteEndTime = currentNote.getStartTime() + currentNote.getDuration() # get end time of current note
      return futureNote.getStartTime() - currentNoteEndTime
