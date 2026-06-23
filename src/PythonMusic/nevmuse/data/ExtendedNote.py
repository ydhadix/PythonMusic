# ExtendedNote.py
#
# ExtendedNote is a wrapper that extends the Note class to include
# a float startTime, float startTimeQuantized, float durationQuantized,
# and int voice.
#
# Adapted from the original Java version of nevmuse by:
# Tim Hirzel, Brian Muller, Brys Sepulveda and Bill Manaris

from music import Note
from functools import total_ordering   # used for compareTo


@total_ordering
class ExtendedNote(Note):   # public class ExtendedNote extends Note implements Comparable
   """
   ExtendedNote is a wrapper that extends the Note class to include
   a float startTime, float startTimeQuantized, float durationQuantized,
   and int voice.
   """

   def __init__(self, noteIn, startTimeIn=None):
      """
      Constructor for objects of class ExtendedNote.
      noteIn is the regular Note object that this will wrap around.
      """

      # initialize parent class
      Note.__init__(self, noteIn.getPitch(), noteIn.getDuration())
      self.setDynamic(noteIn.getDynamic())
      self.setPan(noteIn.getPan())
      self.setLength(noteIn.getLength())

      # add new attributes (for use in PianoRoll.py)
      if startTimeIn is not None:
         self.startTime = float(startTimeIn)
      elif hasattr(noteIn, 'getStartTime'): # If it's an ExtendedNote or has getStartTime
         self.startTime = float(noteIn.getStartTime())
      else:
         self.startTime = 0.0

      # copy properties if noteIn is already an ExtendedNote (for backwards compatibility)
      if isinstance(noteIn, ExtendedNote):
         self.startTimeQuantized = noteIn.getStartTimeQuantized()
         self.durationQuantized = noteIn.getDurationQuantized()
         self.voice = noteIn.getVoice()
      else:
         self.startTimeQuantized = 0.0   # quantized absolute start time aligned to piano roll quantum
         self.durationQuantized = 0.0    # quantized duration of note within piano roll (usually less than actual (recorded) duration value)
         self.voice = -1                 # Initialize to -1 to know whether it has been set

   def __str__(self):
      return (
         f'ExtendedNote(pitch = {self.getPitch()}, startTime = {self.getStartTime()}, '
         f'length = {self.getLength()}, duration = {self.getDuration()}, '
         f'duration quantized = {self.getDurationQuantized()}, '
         f'voice = {self.getVoice()})'
      )

   def __eq__(self, other):
      if not isinstance(other, ExtendedNote):
         # It is safer to return NotImplemented than raise TypeError for __eq__
         return NotImplemented
      else:
         return (self.getStartTime(), self.getFrequency()) == (other.getStartTime(), other.getFrequency())

   def __lt__(self, other):
      if not isinstance(other, ExtendedNote):
         # It is safer to return NotImplemented than raise TypeError for __lt__
         return NotImplemented
      else:
         # Python compares tuples element by element:
         # First compare start_time
         # If start_times are equal, compare frequency
         return (self.getStartTime(), self.getFrequency()) < (other.getStartTime(), other.getFrequency())

   # TODO: do we want to allow comparison to Notes as well? won't there start time always just be 0.0 then?
   # the original casts other to type ExtendedNote first without checking
   def compareTo(self, other):
      """
      This method compares two ExtendedNotes for order.
      Returns a negative integer, zero, or a positive integer as this ExtendedNote is less than,
      equal to, or greater than the specified object.

      Note: To compare we use start time (primary key); if start times are equal, then we use pitch (secondary key).

      Expects other, the object to compare against this ExtendedNote for order.
      Returns a negative integer, zero, or a positive integer if this ExtendedNote is less than,
              equal to, or greater than the specified object
      """
      if not isinstance(other, ExtendedNote) and not isinstance(other, Note):
         raise TypeError(f"Cannot compare ExtendedNote with {type(other)}.")
      else:
         # If self > other, (1 - 0) = 1
         # If self < other, (0 - 1) = -1
         # If self == other, (0 - 0) = 0
         return (self > other) - (self < other)

   def copy(self):
      """
      Returns a deep copy of this ExtendedNote.
      """
      # Uses the copy logic we added to __init__
      return ExtendedNote(self, self.startTime)

   def getStartTime(self):
      """
      Returns absolute start time (from the beginning of the score).
      """
      return self.startTime

   def setStartTime(self, startTime):
      """
      Expects absolute start time (from the beginning of the score).
      """
      self.startTime = startTime

   def getStartTimeQuantized(self):
      """
      Returns absolute start time aligned to piano roll quantum.
      """
      return self.startTimeQuantized

   def setStartTimeQuantized(self, startTimeQuantized):
      """
      Expects absolute start time aligned to piano roll quantum.
      """
      self.startTimeQuantized = startTimeQuantized

   def getDurationQuantized(self):
      """
      Returns quantized duration of note within piano roll (usually less than actual (recorded) duration value).
      """
      return self.durationQuantized

   def setDurationQuantized(self, durationQuantized):
      """
      Expects quantized duration of note within piano roll (usually less than actual (recorded) duration value).
      """
      self.durationQuantized = durationQuantized

   def voiceHasBeenSet(self):
      """
      Returns True if the voice has been set, or False if not."
      """
      return self.voice != -1

   def setVoice(self, voice):
      """
      Sets the voice (int).
      """
      self.voice = int(voice)

   def getVoice(self):
      """
      Returns the voice (int).
      """
      return self.voice

   def toString(self):
      """
      For backwards compatibility.
      In Python, simply use str(extendedNote).
      """
      return str(self)
