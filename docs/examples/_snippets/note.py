# note.py
#
# It demonstrates how to create a class to encapsulate a musical
# note.  (This is a simplified version of Note class found in the
# music library.)
#

from music import *

class Note:

   def __init__(self, pitch=C4, duration=QN, dynamic=85, panning=0.5):
      """Initializes a Note object."""

      self.pitch = pitch        # holds note pitch (0-127)
      self.duration = duration  # holds note duration (QN = 1.0)
      self.dynamic = dynamic    # holds note dynamic (0-127)
      self.panning = panning    # holds note panning (0.0-1.0)

   def getPitch(self):
      """Returns the note's pitch (0-127)."""

      return self.pitch

   def setPitch(self, pitch):
      """Sets the note's pitch (0-127)."""

      # first ensure data integrity, then update
      if 0 <= pitch <= 127:  # is pitch in the right range?
         self.pitch = pitch     # yes, so update value
      else:                  # otherwise let them know
         print("TypeError: Note.setPitch(): pitch ranges from 0 to 127 (got " + str(pitch) + ")")
         #raise TypeError("Note.setPitch(): pitch ranges from 0 to 127 (got " + str(pitch) + ")")

   def getDuration(self):
      """Returns the note's duration."""

      return self.duration

   def setDuration(self, duration):
      """Sets the note's duration (a float)."""

      if type(duration) == type(1.0):    # is duration a float?
         self.duration = float(duration)    # yes, so update value
      else:                  # otherwise let them know
         print("TypeError: Note.setDuration(): duration must be a float (got " + str(duration) + ")")
         # raise TypeError("Note.setDuration(): duration must be a float (got " + str(duration) + ")")

if __name__ == '__main__':

   # create a note
   print("n = Note(C4, QN)")
   n = Note(C4, QN)
   print("n.getPitch() =", n.getPitch())
   print("n.getDuration() =", n.getDuration())