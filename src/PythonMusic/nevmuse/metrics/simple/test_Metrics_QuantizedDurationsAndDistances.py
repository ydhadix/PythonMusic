# test_Metrics_QuantizedDurationsAndDistances.py
#
# Unit tests for Quantized Durations & Distances Metrics.
#
# Usage:
#   python -m unittest src/nevmuse/metrics/simple/test_Metrics_QuantizedDurationsAndDistances.py

import os
import sys
import unittest

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import *
from ...data.PianoRoll import PianoRoll
from .DurationQuantizedMetric import DurationQuantizedMetric
from .DurationDistanceMetric import DurationDistanceMetric
from .DurationQuantizedDistanceMetric import DurationQuantizedDistanceMetric
from .PitchDistanceMetric import PitchDistanceMetric
from .PitchDurationMetric import PitchDurationMetric
from .PitchDurationQuantizedMetric import PitchDurationQuantizedMetric

class TestMetricsQuantizedDurationsAndDistances(unittest.TestCase):
   """
   Test cases for Quantized Durations & Distances Metrics.
   """

   def setUp(self):
      """
      Set up test fixtures with a score designed to test distances and durations.
      """
      self.score = Score("Test Score Distances")
      part = Part("Piano", PIANO, 0)
      
      # Repeated patterns to trigger distance metrics
      # Pattern: C4 (QN), E4 (EN), G4 (EN)
      # Time 0.0
      phrase = Phrase(0.0)
      phrase.addNote(Note(C4, QN))
      phrase.addNote(Note(E4, EN))
      phrase.addNote(Note(G4, EN))
      part.addPhrase(phrase)
      
      # Time 2.0 (same pattern repeated)
      phrase2 = Phrase(2.0)
      phrase2.addNote(Note(C4, QN))
      phrase2.addNote(Note(E4, EN))
      phrase2.addNote(Note(G4, EN))
      part.addPhrase(phrase2)

      # Time 4.0 (variation with different durations but same pitches)
      phrase3 = Phrase(4.0)
      phrase3.addNote(Note(C4, HN))  # Different duration
      phrase3.addNote(Note(E4, EN))
      phrase3.addNote(Note(G4, EN))
      part.addPhrase(phrase3)
      
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

   def test_DurationQuantizedMetric(self):
      self.run_metric_test(DurationQuantizedMetric())

   def test_DurationDistanceMetric(self):
      self.run_metric_test(DurationDistanceMetric())

   def test_DurationQuantizedDistanceMetric(self):
      self.run_metric_test(DurationQuantizedDistanceMetric())

   def test_PitchDistanceMetric(self):
      self.run_metric_test(PitchDistanceMetric())

   def test_PitchDurationMetric(self):
      self.run_metric_test(PitchDurationMetric())

   def test_PitchDurationQuantizedMetric(self):
      self.run_metric_test(PitchDurationQuantizedMetric())

if __name__ == "__main__":
   unittest.main()
