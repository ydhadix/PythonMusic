from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics

class DurationBigramMetric(Metric):
   """
   It implements a Zipf metric capturing proportion of note duration bigrams in a music piece.

   author Bill Manaris
   version 1.2 (February 26, 2007)
   version 1.0 (August 13, 2005)

   NOTE: The original Java source (DurationBigramMetric.java~) included a feature
   for variable localVariabilityWindowSize. However, the base Metric.java class
   hardcodes this to 5. This implementation aligns with the base Metric class and
   ignores the custom window size logic to ensure consistency.
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a DurationBigramMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level           the level of this metric (0 means base metric) - internal use
      """
      super().__init__("DurationBigram", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return DurationBigramMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts the durations of all new notes found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)  # holds the current time slice

      # access all notes with current time slice, identify each melodic bigram, and count it
      for i in range(len(timeSlice)):
         if timeSlice[i] > 0:  # if this is a new note (as opposed to a continuation of an earlier note)
            note = pianoRoll.getNote(timeSlice[i])       # get the note
            duration = note.getDuration()                # get this note's duration
            voice = note.getVoice()                      # get this note's voice
            nextNote = pianoRoll.getNextNoteSameVoice(voice, timeIndex) # get the next note that matches current note's voice

            if nextNote is not None:  # check if there even is a next note
               # Let's combine the durations of the two notes into one value.
               # ... (comment preserved) ...
               # (Note: since duration may range from 0 to say 3.00, we divide by 10 to ensure that the
               #  second duration ends up well into the decimal part.)
               durationBigram = duration + (nextNote.getDuration() / 10.0)   # assmeble duration bigram indentifier
               self.count(durationBigram)                                    # and count it
