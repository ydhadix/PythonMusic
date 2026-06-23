from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll
import math

class ChordDensityMetric(Metric):
   """
   It calculates the density of an harmonic interval.  The density a harmony is calculated using the Density
   Degree Theory from Dr. Orlando Legname. http://www.oneonta.edu/faculty/legnamo/theorist/density/density.html

   author David Johnson and Bill Manaris
   version 1.0 (October 24, 2013)
   """

   CHORD_DENSITIES = [
      1.000000, 16.501386, 9.055972, 5.867546, 4.806131, 3.745936, 9.141450, 2.688768, 7.042207, 4.344963,
      7.655963, 12.623786, 1.642991, 26.118654, 7.263811, 9.564906, 3.954797, 6.261018, 15.489625, 2.304766,
      12.205387, 7.591236, 13.550197, 11.246060, 2.980329, 47.444757, 6.645173, 17.643343, 3.665606, 11.686902,
      29.109401, 4.356628, 23.174682, 14.459999, 25.954542, 10.800142, 5.748990, 91.884162, 6.448410, 34.343034,
      7.148938, 22.852745, 57.048007, 8.553093, 45.590228, 28.465992, 51.207304, 10.663756, 11.368088, 182.003683,
      12.777542, 68.118756, 14.188765, 45.385803, 113.374697, 17.010485, 90.754720, 56.679407, 102.067913, 21.249543,
      22.662411, 363.120136, 25.489455, 136.026668, 28.296429, 90.642899, 226.285752, 33.965895, 181.340138, 113.201112,
      204.005823, 42.444481, 45.275169, 724.833981, 50.932122, 272.019001, 56.564505, 181.275870, 452.261648, 67.930367,
      362.685326, 226.403799, 407.990886, 84.855231, 67.894990
   ]

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a ChordDensityMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("Chord", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return ChordDensityMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts the density of harmonies in a score.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)      # get time slice

      isNewChord = False        # assume there are no new notes in this time slice
      totalDensity = 0.0

      if len(timeSlice) > 0:
         basePitch = pianoRoll.getNote(abs(timeSlice[0])).getPitch()  # find the base pitch to use in interval calculations

         for i in range(len(timeSlice)):
            if timeSlice[i] > 0:  # if this is a new note (as opposed to a continuation)
               isNewChord = True    # so, we have a new chord

            if i > 0:
               note = pianoRoll.getNote(abs(timeSlice[i]))     # get the note (regardless if it's new or continuation)
               pitch = note.getPitch()                         # get the note's pitch
               interval = pitch - basePitch # Calculate the interval from the base tone for each harmony

               # Safety check for interval index bounds
               if 0 <= interval < len(ChordDensityMetric.CHORD_DENSITIES):
                  totalDensity += ChordDensityMetric.CHORD_DENSITIES[interval]

         if isNewChord:   # if this is a new chord...
            if totalDensity > 0:
                densityDegree = 20 * math.log10(totalDensity)
                roundedDensityDegree = int(densityDegree)  # Calc log of total density and cast to an int for rounding
                self.count(float(roundedDensityDegree))    # change density to integer
