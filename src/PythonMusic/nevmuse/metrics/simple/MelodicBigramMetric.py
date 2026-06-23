from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics

class MelodicBigramMetric(Metric):
   """
   It implements a Zipf metric capturing proportion of melodic-bigrams in a music piece.

   author Hector Mojica and Bill Manaris
   version 1.2 (February 26, 2007)
   version 1.1 (Aug 1, 2005)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a MelodicBigramMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("MelodicBigram", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return MelodicBigramMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts all new melodic-bigrams found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)  # holds the current time slice

      # access all notes with current time slice, identify each melodic bigram, and count it
      for i in range(len(timeSlice)):
         if timeSlice[i] > 0:  # if this is a new note (as opposed to a continuation of an earlier note)
            note = pianoRoll.getNote(timeSlice[i])       # get the note
            pitch = note.getPitch()                      # get this note's pitch
            voice = note.getVoice()                      # get this note's voice
            nextNote = pianoRoll.getNextNoteSameVoice(voice, timeIndex) # get the next note that matches current note's voice

            if nextNote is not None:  # check if there even is a next note
               # Let's combine the pitches of the two notes into one value.
               # In particular, the current pitch is stored in the integral part of the double value,
               # whereas next pitch is stored in the decimal part.
               # This produces a unique value for each pitch-pitch combination.
               # Calculating the difference of two such values (i.e., higher-order metrics),
               # still produces a meaningful value (where the integral part is the difference of the two current pitches,
               # and the decimal part is the difference of the two next pitches.
               # (Note: since pitch may range from 0..127, we divide by 1000 to ensure that the
               #  second pitch ends up well into the decimal part.)
               melodicBigram = pitch + (nextNote.getPitch() / 1000.0)   # assmeble melodic bigram indentifier
               self.count(melodicBigram)                                # and count it
