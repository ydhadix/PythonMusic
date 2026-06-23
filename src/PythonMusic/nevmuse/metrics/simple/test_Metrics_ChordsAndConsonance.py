# test_Metrics_ChordsAndConsonance.py
#
# Unit tests for Chords & Consonance Metrics.
#
# Usage:
#   python -m unittest src/nevmuse/metrics/simple/test_Metrics_ChordsAndConsonance.py

import os
import sys
import unittest

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import *
from ...data.PianoRoll import PianoRoll
from .ChordMetric import ChordMetric
from .ChordDensityMetric import ChordDensityMetric
from .ChordDistanceMetric import ChordDistanceMetric
from .ChordNormalizedMetric import ChordNormalizedMetric
from .HarmonicConsonanceMetric import HarmonicConsonanceMetric
from .MelodicConsonanceMetric import MelodicConsonanceMetric

class TestMetricsChordsAndConsonance(unittest.TestCase):
   """
   Test cases for Chords & Consonance Metrics.
   """

   def setUp(self):
      """
      Set up test fixtures with a score designed to test chords and consonance.
      """
      self.score = Score("Test Score Chords")
      
      # Create chords
      # C Major, G Major, A Minor, F Major
      part = Part("Piano", PIANO, 0)
      
      # Chord 1: C Major (C4, E4, G4)
      phrase = Phrase(0.0)
      phrase.addNote(Note(C4, HN))
      part.addPhrase(phrase)
      
      phrase2 = Phrase(0.0)
      phrase2.addNote(Note(E4, HN))
      part.addPhrase(phrase2)
      
      phrase3 = Phrase(0.0)
      phrase3.addNote(Note(G4, HN))
      part.addPhrase(phrase3)
      
      # Chord 2: G Major (G3, B3, D4) at time 2.0
      phrase4 = Phrase(2.0)
      phrase4.addNote(Note(G3, HN))
      part.addPhrase(phrase4)
      
      phrase5 = Phrase(2.0)
      phrase5.addNote(Note(B3, HN))
      part.addPhrase(phrase5)
      
      phrase6 = Phrase(2.0)
      phrase6.addNote(Note(D4, HN))
      part.addPhrase(phrase6)

      # Chord 3: Repeat C Major to test ChordDistance (at time 4.0)
      phrase7 = Phrase(4.0)
      phrase7.addNote(Note(C4, HN))
      part.addPhrase(phrase7)
      
      phrase8 = Phrase(4.0)
      phrase8.addNote(Note(E4, HN))
      part.addPhrase(phrase8)
      
      phrase9 = Phrase(4.0)
      phrase9.addNote(Note(G4, HN))
      part.addPhrase(phrase9)

      self.score.addPart(part)
      
      # Create PianoRoll
      self.pr = PianoRoll(self.score, quantum=0.25)

   def run_metric_test(self, metric):
      """Helper to run standard metric test logic."""
      metric.init()
      
      # Measure each time slice
      for i in range(self.pr.getLength()):
         metric.measureTimeSlice(self.pr, i)
      
      measurement = metric.getMeasurement()
      
      # Get measurement results
      name = metric.getName()
      slope_key = f"{name}_0_Slope"
      r2_key = f"{name}_0_R2"
      
      slope = measurement.get(slope_key)
      r2 = measurement.get(r2_key)
      
      # print(f"Metric: {name}, Slope: {slope}, R2: {r2}")
      
      self.assertIsNotNone(slope, f"{name} Slope should not be None")
      self.assertIsNotNone(r2, f"{name} R2 should not be None")

   def test_ChordMetric(self):
      self.run_metric_test(ChordMetric())

   def test_ChordDensityMetric(self):
      self.run_metric_test(ChordDensityMetric())

   def test_ChordDistanceMetric(self):
      self.run_metric_test(ChordDistanceMetric())

   def test_ChordNormalizedMetric(self):
      self.run_metric_test(ChordNormalizedMetric())

   def test_HarmonicConsonanceMetric(self):
      self.run_metric_test(HarmonicConsonanceMetric())

   def test_MelodicConsonanceMetric(self):
      self.run_metric_test(MelodicConsonanceMetric())

if __name__ == "__main__":
   unittest.main()
