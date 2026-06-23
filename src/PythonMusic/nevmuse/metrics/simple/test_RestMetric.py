# test_RestMetric.py
#
# Unit tests for RestMetric class.
#
# Usage:
#   python -m unittest src/nevmuse/metrics/simple/test_RestMetric.py

import os
import sys
import unittest

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import Score, Part, Phrase, Note, C4
from ...data.PianoRoll import PianoRoll
from .RestMetric import RestMetric


class TestRestMetric(unittest.TestCase):
   """
   Test cases for RestMetric class.
   """

   def setUp(self):
      """
      Set up a simple score and piano roll for testing.
      """
      # Create a score:
      # Note 1: Start 0.0, Dur 1.0.
      # Rest: 1.0 (implicitly, by gap)
      # Note 2: Start 2.0, Dur 1.0.
      self.score = Score("Test Score")
      p = Part("Test Part")
      ph = Phrase(0.0) # Start time 0.0
      ph.addNote(Note(C4, 1.0))
      ph.addNote(Note(C4, 1.0)) # Note: Phrase handles sequential timing automatically in jMusic/music.py?
      # In music.py, Phrase accumulates duration.
      # Note 1 starts at 0.0. Ends at 1.0.
      # Note 2 starts at 1.0. Ends at 2.0.

      # To add a rest, we add a Rest note?
      # Or just set start time?
      # In PythonMusic/jMusic, rests are notes with pitch REST (-2147483648).
      # But PianoRoll handles timing based on score.

      # Let's try adding a rest note explicitly.
      from music import REST
      ph.addNote(Note(REST, 1.0))
      ph.addNote(Note(C4, 1.0))

      # Sequence: Note(1.0), Rest(1.0), Note(1.0).
      # Note 1: Start 0.0.
      # Note 2 (Rest): Start 1.0.
      # Note 3: Start 2.0.

      p.addPhrase(ph)
      self.score.addPart(p)

      # Quantum 0.25
      self.pr = PianoRoll(self.score, 0.25, 7)

      self.metric = RestMetric(0)

   def test_measureTimeSlice(self):
      """Test measuring time slices."""

      # Run for all slices
      for i in range(self.pr.getLength()):
         self.metric.measureTimeSlice(self.pr, i)

      # Analysis:
      # Note 1 (Start 0.0) -> Note 2 (Start 1.0). IOI = 1.0.
      # Note 2 (Start 1.0) -> Note 4 (Start 3.0). IOI = 2.0.
      # Note 3 (Rest) was ignored by PianoRoll.

      hist = self.metric.histogram

      # We expect 1.0 and 2.0.
      self.assertEqual(1.0, hist.get(1.0))
      self.assertEqual(1.0, hist.get(2.0))

if __name__ == "__main__":
   unittest.main()
