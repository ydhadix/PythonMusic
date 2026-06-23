"""
Test suite for PianoRoll quantization with snap-to-nearest-gridline behavior.
Tests that notes snap to nearest quantum boundary, collapsed notes are dropped,
and long notes use continuations (negative indices) instead of splitting.
"""
import sys
import os

# Add src directory to path
srcPath = os.path.join(os.path.dirname(__file__), '../..')
sys.path.insert(0, srcPath)

from music import *
from .PianoRoll import PianoRoll

def testSnapToNearestGridline():
   """Test that notes snap to nearest quantum boundary"""
   score = Score()
   part = Part()
   phrase = Phrase(0.0)

   # Note from 0.1 to 0.9 should snap to 0.0-1.0 with quantum=0.5
   note = Note(C4, 0.8, length=0.8)
   phrase.addNote(note)

   # Manually set start time to 0.1
   phrase.getNoteList()[0]._startTime = 0.1

   part.addPhrase(phrase)
   score.addPart(part)

   pr = PianoRoll(score, quantum=0.5)

   # Should have 2 time slices with ONE note (not two segments)
   assert pr.getNoteCount() == 1, f"Should have 1 note (not split), got {pr.getNoteCount()}"

   # Check first time slice (0.0-0.5) - should have positive index
   slice0 = pr.getTimeSlice(0)
   assert len(slice0) > 0, "First slice should have a note"
   assert slice0[0] > 0, "First slice should have positive index (note starts)"

   note0 = pr.getNote(abs(slice0[0]))
   assert abs(note0.getStartTimeQuantized() - 0.0) < 0.001, \
      f"Note should start at 0.0, got {note0.getStartTimeQuantized()}"
   assert abs(note0.getDurationQuantized() - 1.0) < 0.001, \
      f"Duration should be full 1.0, got {note0.getDurationQuantized()}"

   # Check second time slice (0.5-1.0) - should have negative index (continuation)
   slice1 = pr.getTimeSlice(1)
   assert len(slice1) > 0, "Second slice should have a note"
   assert slice1[0] < 0, "Second slice should have negative index (continuation)"
   assert abs(slice1[0]) == abs(slice0[0]), "Both slices should reference same note"

   print("Snap to nearest gridline test: PASSED")

def testCollapsedNotesDropped():
   """Test that notes collapsing to same boundary are dropped"""
   score = Score()
   part = Part()
   phrase = Phrase(0.0)

   # Note from 0.4 to 0.6 should snap to 0.5-0.5 and be dropped
   # 0.4/0.5 = 0.8 -> rounds to 1 -> 0.5
   # 0.6/0.5 = 1.2 -> rounds to 1 -> 0.5
   note = Note(C4, 0.2, length=0.2)
   phrase.addNote(note)
   phrase.getNoteList()[0]._startTime = 0.4

   part.addPhrase(phrase)
   score.addPart(part)

   pr = PianoRoll(score, quantum=0.5)

   # Should have no notes (dropped)
   assert pr.getNoteCount() == 0, f"Collapsed note should be dropped, got {pr.getNoteCount()} notes"

   print("Collapsed notes dropped test: PASSED")

def testLongNoteContinuation():
   """Test that long notes use continuations instead of splitting"""
   score = Score()
   part = Part()
   phrase = Phrase(0.0)

   # Note from 0.0 to 2.3 should snap to 0.0-2.5
   # 0.0/0.5 = 0.0 -> rounds to 0 -> 0.0
   # 2.3/0.5 = 4.6 -> rounds to 5 -> 2.5
   phrase.addNote(Note(C4, 2.3, length=2.3))

   part.addPhrase(phrase)
   score.addPart(part)

   pr = PianoRoll(score, quantum=0.5)

   # Should have ONE note, not 5 segments
   assert pr.getNoteCount() == 1, f"Should have 1 note, got {pr.getNoteCount()}"

   # Check time slices
   # Slice 0: positive index (note starts)
   # Slices 1-4: negative index (continuations)
   slice0 = pr.getTimeSlice(0)
   assert len(slice0) > 0, "First slice should have a note"
   assert slice0[0] > 0, "First slice should be positive (note start)"
   noteIndex = slice0[0]

   for i in range(1, 5):
      sliceI = pr.getTimeSlice(i)
      assert len(sliceI) > 0, f"Slice {i} should have a note"
      assert sliceI[0] < 0, f"Slice {i} should be negative (continuation)"
      assert abs(sliceI[0]) == noteIndex, f"Slice {i} should reference same note"

   # Verify the note has correct quantized duration
   note = pr.getNote(noteIndex)
   assert abs(note.getDurationQuantized() - 2.5) < 0.001, \
      f"Note should have duration 2.5, got {note.getDurationQuantized()}"

   print("Long note continuation test: PASSED")

def testMidpointRoundsDown():
   """Test that notes at exact midpoint between boundaries round down"""
   score = Score()
   part = Part()
   phrase = Phrase(0.0)

   # Note from 0.25 to 0.75 should snap to 0.0-0.5 (not 0.5-1.0)
   # 0.25/0.5 = 0.5 -> rounds DOWN to 0 -> 0.0 (midpoint rule)
   # 0.75/0.5 = 1.5 -> rounds DOWN to 1 -> 0.5 (midpoint rule)
   note = Note(C4, 0.5, length=0.5)
   phrase.addNote(note)
   phrase.getNoteList()[0]._startTime = 0.25

   part.addPhrase(phrase)
   score.addPart(part)

   pr = PianoRoll(score, quantum=0.5)

   # Should have ONE note
   assert pr.getNoteCount() == 1, f"Should have 1 note, got {pr.getNoteCount()}"

   # Check that it starts at time slice 0 (0.0-0.5), not time slice 1 (0.5-1.0)
   slice0 = pr.getTimeSlice(0)
   assert len(slice0) > 0, "First slice should have the note"
   assert slice0[0] > 0, "First slice should have positive index (note start)"

   note0 = pr.getNote(abs(slice0[0]))
   assert abs(note0.getStartTimeQuantized() - 0.0) < 0.001, \
      f"Note should start at 0.0 (midpoint rounds down), got {note0.getStartTimeQuantized()}"
   assert abs(note0.getDurationQuantized() - 0.5) < 0.001, \
      f"Note should have duration 0.5, got {note0.getDurationQuantized()}"

   print("Midpoint rounds down test: PASSED")

if __name__ == "__main__":
   print("Running PianoRoll Quantization Tests...")
   testSnapToNearestGridline()
   testCollapsedNotesDropped()
   testLongNoteContinuation()
   testMidpointRoundsDown()
   print("\nAll PianoRoll quantization tests PASSED!")
