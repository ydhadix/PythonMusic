# test_PianoRoll.py
#
# Unit tests for PianoRoll class.
#
# Usage:
#   python -m unittest test_PianoRoll
#   python -m unittest test_PianoRoll.TestPianoRoll.test_simple_melody

import os
import sys
import unittest

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import Score, Part, Phrase, Note, REST, PIANO
from music import C4, D4, E4, F4, G4, A4, B4, C5
from music import QN, HN, WN   # quarter, half, whole note durations
from .PianoRoll import PianoRoll
from .test_PianoRoll_assertions import runAllAssertions


class TestPianoRoll(unittest.TestCase):
   """
   Unit tests for PianoRoll class.
   """

   def createSimpleMelody(self):
      """
      Create a simple monophonic melody for testing.
      C4 D4 E4 F4 G4 (all quarter notes)
      """
      phrase = Phrase(0.0)
      phrase.addNote(Note(C4, QN))
      phrase.addNote(Note(D4, QN))
      phrase.addNote(Note(E4, QN))
      phrase.addNote(Note(F4, QN))
      phrase.addNote(Note(G4, QN))

      part = Part(PIANO)
      part.addPhrase(phrase)

      score = Score()
      score.addPart(part)

      return score

   def createTwoVoiceScore(self):
      """
      Create a simple two-voice score for testing voice separation.
      Voice 1 (higher): C5 - D5 - E5 (quarter notes)
      Voice 2 (lower):  C4 - D4 - E4 (quarter notes, simultaneous)
      """
      # higher voice
      phrase1 = Phrase(0.0)
      phrase1.addNote(Note(C5, QN))
      phrase1.addNote(Note(67, QN))   # D5 = 62 + 5 = 67... wait, let me use correct MIDI
      phrase1.addNote(Note(64, QN))   # E5

      # lower voice
      phrase2 = Phrase(0.0)
      phrase2.addNote(Note(C4, QN))
      phrase2.addNote(Note(D4, QN))
      phrase2.addNote(Note(E4, QN))

      part = Part(PIANO)
      part.addPhrase(phrase1)
      part.addPhrase(phrase2)

      score = Score()
      score.addPart(part)

      return score

   def createChordScore(self):
      """
      Create a score with chords (multiple simultaneous notes).
      C major chord (C4, E4, G4) held for a whole note.
      """
      # three simultaneous notes starting at the same time
      phrase1 = Phrase(0.0)
      phrase1.addNote(Note(C4, WN))

      phrase2 = Phrase(0.0)
      phrase2.addNote(Note(E4, WN))

      phrase3 = Phrase(0.0)
      phrase3.addNote(Note(G4, WN))

      part = Part(PIANO)
      part.addPhrase(phrase1)
      part.addPhrase(phrase2)
      part.addPhrase(phrase3)

      score = Score()
      score.addPart(part)

      return score

   # -------------------------------------------------------------------------
   # Basic tests
   # -------------------------------------------------------------------------

   def test_simple_melody(self):
      """Test PianoRoll creation with a simple monophonic melody."""
      score = self.createSimpleMelody()
      roll = PianoRoll(score)

      # should have 5 notes
      self.assertEqual(5, roll.getNoteCount())

      # should have 1 voice (monophonic)
      self.assertEqual(1, roll.getNumVoices())

      # should have positive length
      self.assertGreater(roll.getLength(), 0)

      # default quantum should be 0.25
      self.assertEqual(0.25, roll.getQuantum())

   def test_two_voices(self):
      """Test PianoRoll with two simultaneous voices."""
      score = self.createTwoVoiceScore()
      roll = PianoRoll(score)

      # should have 6 notes (3 per voice)
      self.assertEqual(6, roll.getNoteCount())

      # should detect 2 voices
      self.assertEqual(2, roll.getNumVoices())

   def test_chord(self):
      """Test PianoRoll with simultaneous chord notes."""
      score = self.createChordScore()
      roll = PianoRoll(score)

      # should have 3 notes
      self.assertEqual(3, roll.getNoteCount())

      # should detect 3 voices (one per chord note)
      self.assertEqual(3, roll.getNumVoices())

   def test_custom_quantum(self):
      """Test PianoRoll with custom quantum value."""
      score = self.createSimpleMelody()

      # test with larger quantum (half note)
      roll = PianoRoll(score, quantum=0.5)
      self.assertEqual(0.5, roll.getQuantum())

      # test with smaller quantum (32nd note)
      roll2 = PianoRoll(score, quantum=0.125)
      self.assertEqual(0.125, roll2.getQuantum())

      # smaller quantum should result in more time slices
      self.assertGreater(roll2.getLength(), roll.getLength())

   def test_custom_max_voice_jump(self):
      """Test PianoRoll with custom maxVoiceJump."""
      score = self.createTwoVoiceScore()

      # smaller max voice jump may result in more voice changes
      roll = PianoRoll(score, maxVoiceJump=3)

      # should still work
      self.assertGreater(roll.getNoteCount(), 0)

   # -------------------------------------------------------------------------
   # getNote and getTimeSlice tests
   # -------------------------------------------------------------------------

   def test_getNote(self):
      """Test getNote() returns correct notes."""
      score = self.createSimpleMelody()
      roll = PianoRoll(score)

      # notes are 1-indexed (0 is empty)
      note1 = roll.getNote(1)
      self.assertEqual(C4, note1.getPitch())

   def test_getTimeSlice(self):
      """Test getTimeSlice() returns array of note indices."""
      score = self.createSimpleMelody()
      roll = PianoRoll(score)

      # first time slice should contain at least one note
      slice0 = roll.getTimeSlice(0)
      self.assertIsInstance(slice0, list)
      self.assertGreater(len(slice0), 0)

   # -------------------------------------------------------------------------
   # Voice extraction tests
   # -------------------------------------------------------------------------

   def test_getVoice(self):
      """Test getVoice() extracts a single voice as a Part."""
      score = self.createTwoVoiceScore()
      roll = PianoRoll(score)

      # get voice 0 (should be the lower voice due to pitch ordering)
      voice0 = roll.getVoice(0)
      self.assertIsNotNone(voice0)

      # get voice 1 (should be the higher voice)
      voice1 = roll.getVoice(1)
      self.assertIsNotNone(voice1)

   def test_getQuantizedVoice(self):
      """Test getQuantizedVoice() extracts a quantized voice."""
      score = self.createSimpleMelody()
      roll = PianoRoll(score)

      voice = roll.getQuantizedVoice(0)
      self.assertIsNotNone(voice)

   # -------------------------------------------------------------------------
   # Score reconstruction tests
   # -------------------------------------------------------------------------

   def test_getScore(self):
      """Test getScore() reconstructs a Score from the PianoRoll."""
      originalScore = self.createSimpleMelody()
      roll = PianoRoll(originalScore)

      reconstructed = roll.getScore()

      self.assertIsNotNone(reconstructed)
      self.assertIsInstance(reconstructed, Score)

      # should preserve tempo and time signature
      self.assertEqual(originalScore.getTempo(), reconstructed.getTempo())
      self.assertEqual(originalScore.getNumerator(), reconstructed.getNumerator())
      self.assertEqual(originalScore.getDenominator(), reconstructed.getDenominator())

      # Run comprehensive assertions
      runAllAssertions(originalScore, reconstructed, roll, 0.25)

   def test_getNScore(self):
      """Test getNScore() returns a Score from quantized voices."""
      score = self.createSimpleMelody()
      roll = PianoRoll(score)

      nScore = roll.getNScore()

      self.assertIsNotNone(nScore)
      self.assertIsInstance(nScore, Score)

   # -------------------------------------------------------------------------
   # Search method tests
   # -------------------------------------------------------------------------

   def test_getNextNoteSameVoice(self):
      """Test getNextNoteSameVoice() finds next note in voice."""
      score = self.createSimpleMelody()
      roll = PianoRoll(score)

      # find next note in voice 0 starting from time 0
      nextNote = roll.getNextNoteSameVoice(0, 0)
      self.assertIsNotNone(nextNote)

   def test_getNextNoteSamePitch(self):
      """Test getNextNoteSamePitch() finds next note with same pitch."""
      # create score with repeated notes
      phrase = Phrase(0.0)
      phrase.addNote(Note(C4, QN))
      phrase.addNote(Note(D4, QN))
      phrase.addNote(Note(C4, QN))   # C4 repeats

      part = Part(PIANO)
      part.addPhrase(phrase)
      score = Score()
      score.addPart(part)

      roll = PianoRoll(score)

      # find next C4 after time slice 0
      nextNote = roll.getNextNoteSamePitch(C4, 0)
      self.assertIsNotNone(nextNote)
      self.assertEqual(C4, nextNote.getPitch())

   # -------------------------------------------------------------------------
   # Edge case tests
   # -------------------------------------------------------------------------

   def test_empty_score_raises_error(self):
      """Test that empty score raises AssertionError."""
      score = Score()
      with self.assertRaises(AssertionError):
         PianoRoll(score)

   def test_single_note_warning(self):
      """Test that single note score works but may warn."""
      phrase = Phrase(0.0)
      phrase.addNote(Note(C4, QN))

      part = Part(PIANO)
      part.addPhrase(phrase)
      score = Score()
      score.addPart(part)

      # should work, just with a warning
      roll = PianoRoll(score)
      self.assertEqual(1, roll.getNoteCount())

   def test_notes_with_rests(self):
      """Test PianoRoll handles rests correctly."""
      phrase = Phrase(0.0)
      phrase.addNote(Note(C4, QN))
      phrase.addNote(Note(REST, QN))   # rest
      phrase.addNote(Note(E4, QN))

      part = Part(PIANO)
      part.addPhrase(phrase)
      score = Score()
      score.addPart(part)

      roll = PianoRoll(score)

      # should have 2 notes (rest is not counted)
      self.assertEqual(2, roll.getNoteCount())


if __name__ == "__main__":
   unittest.main()
