# test_ExtendedNote.py
#
# Unit tests for ExtendedNote class.
# Mirrors the original Java ExtendedNoteTest.java tests.
#
# Usage:
#   python -m unittest test_ExtendedNote
#   python -m unittest test_ExtendedNote.TestExtendedNote.test_compareTo_less_start_time

import os
import sys
import unittest

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import Note, C3, C4, C5
from .ExtendedNote import ExtendedNote


class TestExtendedNote(unittest.TestCase):
   """
   Test cases for ExtendedNote class.
   Mirrors the Java ExtendedNoteTest.java test cases.
   """

   def setUp(self):
      """
      Set up test fixtures.
      Called before every test case method.

      Creates four ExtendedNotes for testing:
        extendedA: C4, duration=0.25, startTime=1.0
        extendedB: C5, duration=0.25, startTime=2.0
        extendedC: C3, duration=0.25, startTime=1.0
        extendedD: C5, duration=0.25, startTime=1.0
      """
      self.extendedA = ExtendedNote(Note(C4, 0.25), 1.0)
      self.extendedB = ExtendedNote(Note(C5, 0.25), 2.0)
      self.extendedC = ExtendedNote(Note(C3, 0.25), 1.0)
      self.extendedD = ExtendedNote(Note(C5, 0.25), 1.0)

   def tearDown(self):
      """
      Tear down test fixtures.
      Called after every test case method.
      """
      pass

   # -------------------------------------------------------------------------
   # Tests mirroring Java ExtendedNoteTest.java
   # -------------------------------------------------------------------------

   def test_compareTo_less_start_time(self):
      """
      Test compareTo when this note has earlier start time.
      Java: testTestComparedToLessStartTime()
      """
      self.assertEqual(-1, self.extendedA.compareTo(self.extendedB))

   def test_compareTo_greater_start_time(self):
      """
      Test compareTo when this note has later start time.
      Java: testTestComparedToGreaterStartTime()
      """
      self.assertEqual(1, self.extendedB.compareTo(self.extendedA))

   def test_compareTo_equal_start_time_less_pitch(self):
      """
      Test compareTo when start times are equal and this note has lower pitch.
      Java: testTestComparedToEqualStartTimeLessPitch()
      """
      self.assertEqual(-1, self.extendedC.compareTo(self.extendedA))

   def test_compareTo_equal_start_time_greater_pitch(self):
      """
      Test compareTo when start times are equal and this note has higher pitch.
      Java: testTestComparedToEqualStartTimeGreaterPitch()
      """
      self.assertEqual(1, self.extendedA.compareTo(self.extendedC))

   def test_compareTo_equal_start_time_equal_pitch(self):
      """
      Test compareTo when both start time and pitch are equal.
      Java: testTestComparedToEqualStartTimeEqualPitch()
      """
      self.assertEqual(0, self.extendedA.compareTo(self.extendedA))

   # -------------------------------------------------------------------------
   # Additional Python-specific tests
   # -------------------------------------------------------------------------

   def test_less_than_operator(self):
      """Test Python < operator."""
      self.assertTrue(self.extendedA < self.extendedB)   # earlier start time
      self.assertTrue(self.extendedC < self.extendedA)   # same start, lower pitch
      self.assertFalse(self.extendedB < self.extendedA)   # later start time

   def test_greater_than_operator(self):
      """Test Python > operator."""
      self.assertTrue(self.extendedB > self.extendedA)   # later start time
      self.assertTrue(self.extendedA > self.extendedC)   # same start, higher pitch
      self.assertFalse(self.extendedA > self.extendedB)   # earlier start time

   def test_equality_operator(self):
      """Test Python == operator."""
      # same note should equal itself
      self.assertEqual(self.extendedA, self.extendedA)
      # different notes with same start time and pitch should be equal
      anotherA = ExtendedNote(Note(C4, 0.25), 1.0)
      self.assertEqual(self.extendedA, anotherA)
      # different start times should not be equal
      self.assertNotEqual(self.extendedA, self.extendedB)
      # same start time, different pitch should not be equal
      self.assertNotEqual(self.extendedA, self.extendedC)

   def test_sorting(self):
      """Test that a list of ExtendedNotes sorts correctly by (startTime, pitch)."""
      notes = [self.extendedB, self.extendedD, self.extendedA, self.extendedC]
      notes.sort()
      # expected order: C (1.0, C3), A (1.0, C4), D (1.0, C5), B (2.0, C5)
      self.assertEqual(self.extendedC, notes[0])   # startTime=1.0, C3
      self.assertEqual(self.extendedA, notes[1])   # startTime=1.0, C4
      self.assertEqual(self.extendedD, notes[2])   # startTime=1.0, C5
      self.assertEqual(self.extendedB, notes[3])   # startTime=2.0, C5

   def test_getters_and_setters(self):
      """Test getter and setter methods."""
      note = ExtendedNote(Note(C4, 0.5), 0.0)

      # test startTime
      self.assertEqual(0.0, note.getStartTime())
      note.setStartTime(1.5)
      self.assertEqual(1.5, note.getStartTime())

      # test startTimeQuantized
      self.assertEqual(0.0, note.getStartTimeQuantized())
      note.setStartTimeQuantized(1.0)
      self.assertEqual(1.0, note.getStartTimeQuantized())

      # test durationQuantized
      self.assertEqual(0.0, note.getDurationQuantized())
      note.setDurationQuantized(0.25)
      self.assertEqual(0.25, note.getDurationQuantized())

      # test voice
      self.assertEqual(-1, note.getVoice())
      self.assertFalse(note.voiceHasBeenSet())
      note.setVoice(2)
      self.assertEqual(2, note.getVoice())
      self.assertTrue(note.voiceHasBeenSet())

   def test_copy(self):
      """Test copy() method creates a proper deep copy."""
      original = ExtendedNote(Note(C4, 0.5), 1.0)
      original.setStartTimeQuantized(1.0)
      original.setDurationQuantized(0.5)
      original.setVoice(3)

      copy = original.copy()

      # verify copy has same values
      self.assertEqual(original.getPitch(), copy.getPitch())
      self.assertEqual(original.getDuration(), copy.getDuration())
      self.assertEqual(original.getStartTime(), copy.getStartTime())
      self.assertEqual(original.getStartTimeQuantized(), copy.getStartTimeQuantized())
      self.assertEqual(original.getDurationQuantized(), copy.getDurationQuantized())
      self.assertEqual(original.getVoice(), copy.getVoice())

      # verify modifying copy doesn't affect original
      copy.setVoice(5)
      self.assertEqual(3, original.getVoice())
      self.assertEqual(5, copy.getVoice())

   def test_toString(self):
      """Test toString() and __str__() methods."""
      note = ExtendedNote(Note(C4, 0.25), 1.0)
      note.setVoice(0)

      strRepr = str(note)
      self.assertIn("ExtendedNote", strRepr)
      self.assertIn("pitch", strRepr)
      self.assertIn("startTime", strRepr)
      self.assertIn("voice", strRepr)

      # toString() should return same as str()
      self.assertEqual(strRepr, note.toString())


if __name__ == "__main__":
   unittest.main()
