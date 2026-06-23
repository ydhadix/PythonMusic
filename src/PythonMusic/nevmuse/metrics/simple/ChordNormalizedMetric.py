from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics
from ...data.PianoRoll import PianoRoll

class ChordNormalizedMetric(Metric):
   """
   It calculates the rank-frequency distribution of chords within a music piece.  It approximates chords
   by computing the key-centerderness of each harmonic set.

   author Bill Manaris and John Emerson
   version 1.2 (February 26, 2007)
   version 1.0 (July 30, 2005)
   """

   # contains values corresponding to the 12 chromatic tones
   TONES = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a ChordNormalizedMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("Chord", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)
      self.counts = [0.0] * 12   # contains the number of occurrences of the corresponding tones

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return ChordNormalizedMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts all new pitches found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)      # get time slice

      # initialize tone counts
      for i in range(12):
         self.counts[i] = 0.0

      isNewChord = False        # assume there are no new notes in this time slice

      for i in range(len(timeSlice)):
         if timeSlice[i] > 0:  # if this is a new note (as opposed to a continuation)
            isNewChord = True    # so, we have a new chord

         note = pianoRoll.getNote(abs(timeSlice[i]))     # get the note (regardless if it's new or continuation)
         pitch = note.getPitch()                         # get the note's pitch
         self.counts[pitch % 12] += 1                    # incement the count for this tone

      if isNewChord:   # if this is a new chord...
         # construct chord identifier
         place = 0.000001   # initialize
         chordID = 0.0

         for i in range(len(self.TONES)):
            if self.counts[i] > 0:
               chordID += self.TONES[i] * place    # concatenate this tone value
               place *= 100                        # shift place by two decimal digits to the left

         # now, chordID contains every tone sounding in the time slice
         self.count(float(chordID))    # so, let's count it
