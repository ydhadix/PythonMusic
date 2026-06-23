from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll

class HarmonicConsonanceMetric(Metric):
   """
   It implements a Zipf metric capturing the proportion of harmonic consonance in a music piece.

   author   Hector Mojica, John Emerson, Luca Pellicoro, and Bill Manaris
   version 1.2 (February 26, 2007)
   version 1.0 (July 29, 2005)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a HarmonicConsonanceMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("HarmonicConsonance", ZipfMetrics.SIMPLE, ZipfMetrics.BY_SIZE, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return HarmonicConsonanceMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      Increments the corresponding count for each pitch duration in the current time slice.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex  the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)   # holds the current time slice

      # count all combinations of harmonic consonance within this time slice
      for i in range(len(timeSlice)):
         if timeSlice[i] > 0:   # if this is a new note...
            currentNote = pianoRoll.getNote(timeSlice[i])    # get it

            # count harmonic consonance between this note and every higher pitched note
            for j in range(i + 1, len(timeSlice)):
               nextNote = pianoRoll.getNote(abs(timeSlice[j]))       # get the next note
               interval = nextNote.getPitch() - currentNote.getPitch()  # calculate interval
               self.countConsonance(interval)

         if timeSlice[i] < 0:   # if this a continuing note...
            currentNote = pianoRoll.getNote(abs(timeSlice[i]))  # get it

            # count harmonic consonance between this note and every NEW higher pitched note
            # (if a higher pitched note is a continuation, it has been accounted for already)
            for j in range(i + 1, len(timeSlice)):
               if timeSlice[j] > 0:   # a new highe pitched note?
                  nextNote = pianoRoll.getNote(timeSlice[j])                        # get the next note
                  interval = abs(nextNote.getPitch() - currentNote.getPitch())      # calculate interval
                  self.countConsonance(interval)                                    # and count it

      # Now, remove all "last event" entries from histograms
      self.removeHigherOrderLastEvents()

   def countConsonance(self, interval):
      """
      Calculate the consonance rank of the interval and count it.

      param interval    the interval
      """
      rank = interval % 12

      if rank == 0:    # unison
         self.count(1.0)
      elif rank == 7:  # perfect fifth
         self.count(2.0)
      elif rank == 5:  # perfect fourth
         self.count(3.0)
      elif rank == 4:  # major third
         self.count(4.0)
      elif rank == 9:  # major sixth
         self.count(5.0)
      elif rank == 3:  # minor third
         self.count(6.0)
      elif rank == 8:  # minor sixth
         self.count(7.0)
      elif rank == 2:  # major second
         self.count(8.0)
      elif rank == 10: # minor seventh
         self.count(9.0)
      elif rank == 11: # major seventh
         self.count(10.0)
      elif rank == 1:  # minor second
         self.count(11.0)
      elif rank == 6:  # tritone
         self.count(12.0)
