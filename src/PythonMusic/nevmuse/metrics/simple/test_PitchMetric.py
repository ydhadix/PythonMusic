# test_PitchMetric.py
#
# Unit tests for PitchMetric class.
#
# Usage:
#   python -m unittest src/nevmuse/metrics/simple/test_PitchMetric.py

import os
import sys
import unittest

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import Score, Part, Phrase, Note, C4, D4, E4
from ...data.PianoRoll import PianoRoll
from .PitchMetric import PitchMetric


class TestPitchMetric(unittest.TestCase):
   """
   Test cases for PitchMetric class.
   """

   def setUp(self):
      """
      Set up a simple score and piano roll for testing.
      """
      # Create a score: C4, D4, E4 sequential
      self.score = Score("Test Score")
      p = Part("Test Part")
      ph = Phrase()
      ph.addNote(Note(C4, 1.0)) # Pitch 60
      ph.addNote(Note(D4, 1.0)) # Pitch 62
      ph.addNote(Note(E4, 1.0)) # Pitch 64
      p.addPhrase(ph)
      self.score.addPart(p)
      
      # Quantum 0.25 (16th note). 1.0 duration = 4 slices.
      self.pr = PianoRoll(self.score, 0.25, 7)
      
      self.metric = PitchMetric(1) # 1 higher order level

   def test_measureTimeSlice(self):
      """Test measuring time slices."""
      
      # The score has 3 notes.
      # Slice 0: Start of C4. (Index > 0)
      # Slice 1-3: Continuation of C4 (Index < 0)
      # Slice 4: Start of D4.
      # ...
      
      # Measure all slices
      for i in range(self.pr.getLength()):
         self.metric.measureTimeSlice(self.pr, i)
         
      # Expected:
      # Base level: 60 counted once, 62 counted once, 64 counted once.
      hist = self.metric.histogram
      self.assertEqual(1.0, hist.get(60.0))
      self.assertEqual(1.0, hist.get(62.0))
      self.assertEqual(1.0, hist.get(64.0))
      
      # Higher Order (Level 1):
      # Changes: 62-60=2, 64-62=2.
      # So 2.0 counted twice.
      ho = self.metric.higherOrder
      self.assertEqual(2.0, ho.histogram.get(2.0))

   def test_measurement_output(self):
      """Test getting measurement output."""
      for i in range(self.pr.getLength()):
         self.metric.measureTimeSlice(self.pr, i)
         
      m = self.metric.getMeasurement()
      
      # Should have Pitch_0_Slope, Pitch_0_R2, etc.
      slope0 = m.get("Pitch_0_Slope")
      self.assertIsNotNone(slope0)
      
      slope1 = m.get("Pitch_1_Slope")
      self.assertIsNotNone(slope1)

if __name__ == "__main__":
   unittest.main()
