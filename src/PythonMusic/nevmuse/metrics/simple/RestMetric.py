
from ..Metric import Metric
from ..ZipfMetrics import ZipfMetrics

class RestMetric(Metric):
   """
   It implements a Zipf metric capturing proportion of rest durations in a music piece.

   NOTE:  This is very similar to PitchDistance except it uses voices.

   author John Emerson and Bill Manaris
   version 1.2 (February 26, 2007)
   version 1.1 (July 29, 2005)
   version 1.0 (June 7, 2005)
   """

   def __init__(self, numHigherOrder=0, level=0):
      """
      It constructs a RestMetric object for rank-frequency distribution.

      param numHigherOrder  the number of metric levels to calculate (0 means only base metric)
      param level  the level of this metric (0 means base metric). Used internally by recursion.
      """
      super().__init__("Rest", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, level, numHigherOrder)

   def cloneHigherOrder(self):
      """
      It returns a higher-order instance of this Metric class.
      """
      return RestMetric(self.numHigherOrder, self.level + 1)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      It counts all rest durations found in the specified time slice of the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  timeIndex   the index of the current time slice within the piano roll
      """
      assert timeIndex < pianoRoll.getLength(), "Attempted to access a time slice beyond the end of the piano roll!"

      timeSlice = pianoRoll.getTimeSlice(timeIndex)  # holds the current time slice

      # access all notes with current time slice
      for noteIndex in timeSlice:
         if noteIndex > 0:  # if this is a new note (as opposed a continuation of an earlier note)
            currentNote = pianoRoll.getNote(noteIndex) # get the note
            voice = currentNote.getVoice()             # get this note's voice

            # get the future note with the same voice
            futureNote = pianoRoll.getNextNoteSameVoice(voice, timeIndex)

            if futureNote is not None:    # if there is such a note...
               currentNoteStartTimeQuantized = currentNote.getStartTimeQuantized()  # this note's start time
               futureNoteStartTimeQuantized = futureNote.getStartTimeQuantized()    # the future note's start time

               # if there is a rest between the two notes (or rather, if they don't start at the same time)
               # Note: Original Java code calculates onset-to-onset interval here, despite the name "RestMetric".
               if currentNoteStartTimeQuantized != futureNoteStartTimeQuantized:
                  restDuration = futureNoteStartTimeQuantized - currentNoteStartTimeQuantized  # get rest duration
                  self.count(float(restDuration))                                              # and count it
