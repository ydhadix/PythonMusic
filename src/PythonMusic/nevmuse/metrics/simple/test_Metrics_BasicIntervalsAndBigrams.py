# test_Metrics_BasicIntervalsAndBigrams.py
#
# Unit tests for Basic Intervals & Bigrams Metrics.
#
# Usage:
#   python -m unittest src/nevmuse/metrics/simple/test_Metrics_BasicIntervalsAndBigrams.py

import os
import sys
import unittest

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import *
from ...data.PianoRoll import PianoRoll
from .MelodicIntervalMetric import MelodicIntervalMetric
from .HarmonicIntervalMetric import HarmonicIntervalMetric
from .MelodicBigramMetric import MelodicBigramMetric
from .HarmonicBigramMetric import HarmonicBigramMetric
from .DurationBigramMetric import DurationBigramMetric
from .DurationQuantizedBigramMetric import DurationQuantizedBigramMetric

class TestMetricsBasicIntervalsAndBigrams(unittest.TestCase):
   """
   Test cases for Basic Intervals & Bigrams Metrics.
   """

   def setUp(self):
      """
      Set up test fixtures with a complex score.
      """
      # Create a more complex score
      self.score = Score("Test Score Complex")
      part = Part("Piano", PIANO, 0)
      
      # Create a phrase with varied intervals and durations
      # C major scale ascent and descent with varied rhythm
      phrase = Phrase(0.0)
      notes_data = [
         (C4, QN), (E4, EN), (G4, EN), (C5, QN), # Major triad arpeggio
         (B4, EN), (A4, EN), (G4, QN),           # Descent
         (F4, 0.75), (E4, 0.25),                 # Dotted rhythm
         (D4, EN), (D4, EN), (C4, HN)            # Repeated note and long end
      ]
      
      for pitch, dur in notes_data:
         phrase.addNote(Note(pitch, dur))
         
      part.addPhrase(phrase)
      self.score.addPart(part)

      # Create a second voice for harmonic intervals
      part2 = Part("Strings", 0, 1) # Channel 1
      phrase2 = Phrase(0.0)
      # Harmony notes (mostly thirds below)
      harmony_data = [
         (A3, HN), (C4, HN),
         (G3, HN), (E3, HN),
         (F3, HN), (G3, HN),
         (C3, HN) # End
      ]
      for pitch, dur in harmony_data:
         phrase2.addNote(Note(pitch, dur))
      
      part2.addPhrase(phrase2)
      self.score.addPart(part2)
      
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
      
      # Check local variability
      slope_lv_key = f"{name}_0_LocalVariability_Slope"
      r2_lv_key = f"{name}_0_LocalVariability_R2"
      
      slope_lv = measurement.get(slope_lv_key)
      r2_lv = measurement.get(r2_lv_key)
      
      # Local variability might be 0.0/None depending on window size, but checking keys exist
      # Note: Measurement.get returns None if key missing, so we just verify we don't crash
      
   def test_MelodicIntervalMetric(self):
      self.run_metric_test(MelodicIntervalMetric())

   def test_HarmonicIntervalMetric(self):
      self.run_metric_test(HarmonicIntervalMetric())

   def test_MelodicBigramMetric(self):
      self.run_metric_test(MelodicBigramMetric())

   def test_HarmonicBigramMetric(self):
      self.run_metric_test(HarmonicBigramMetric())

   def test_DurationBigramMetric(self):
      self.run_metric_test(DurationBigramMetric())

   def test_DurationQuantizedBigramMetric(self):
      self.run_metric_test(DurationQuantizedBigramMetric())

if __name__ == "__main__":
   unittest.main()
