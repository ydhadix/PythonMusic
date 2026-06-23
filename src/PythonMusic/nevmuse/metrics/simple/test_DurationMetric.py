# test_DurationMetric.py
#
# Unit tests for DurationMetric class.
#
# Usage:
#   python -m unittest src/nevmuse/metrics/simple/test_DurationMetric.py

import os
import sys
import unittest

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import Score, Part, Phrase, Note, C4
from ...data.PianoRoll import PianoRoll
from .DurationMetric import DurationMetric


class TestDurationMetric(unittest.TestCase):
   """
   Test cases for DurationMetric class.
   """

   def setUp(self):
      """
      Set up a simple score and piano roll for testing.
      """
      # Create a score: C4 1.0, C4 2.0, C4 0.5
      self.score = Score("Test Score")
      p = Part("Test Part")
      ph = Phrase()
      ph.addNote(Note(C4, 1.0))
      ph.addNote(Note(C4, 2.0))
      ph.addNote(Note(C4, 0.5))
      p.addPhrase(ph)
      self.score.addPart(p)

      # Quantum 0.25
      self.pr = PianoRoll(self.score, 0.25, 7)

      self.metric = DurationMetric(1) # 1 higher order level

   def test_measureTimeSlice(self):
      """Test measuring time slices."""

      # Measure all slices
      for i in range(self.pr.getLength()):
         self.metric.measureTimeSlice(self.pr, i)

      # Expected:
      # Durations: 1.0, 2.0, 0.5.
      # Base level counts: {1.0: 1, 2.0: 1, 0.5: 1}
      hist = self.metric.histogram
      self.assertEqual(1.0, hist.get(1.0))
      self.assertEqual(1.0, hist.get(2.0))
      self.assertEqual(1.0, hist.get(0.5))

      # Higher Order (Level 1):
      # Changes: 2.0 - 1.0 = 1.0
      # 0.5 - 2.0 = -1.5
      ho = self.metric.higherOrder
      self.assertEqual(1.0, ho.histogram.get(1.0))
      self.assertEqual(1.0, ho.histogram.get(-1.5))

if __name__ == "__main__":
   unittest.main()
