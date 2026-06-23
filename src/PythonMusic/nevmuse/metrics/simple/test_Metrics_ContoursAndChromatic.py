# test_Metrics_ContoursAndChromatic.py
#
# Unit tests for Contours & Chromatic Metrics.
#
# Usage:
#   python -m unittest src/nevmuse/metrics/simple/test_Metrics_ContoursAndChromatic.py

import os
import sys
import unittest

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import *
from ...data.PianoRoll import PianoRoll
from .ContourMelodyPitchMetric import ContourMelodyPitchMetric
from .ContourMelodyDurationMetric import ContourMelodyDurationMetric
from .ContourMelodyDurationQuantizedMetric import ContourMelodyDurationQuantizedMetric
from .ContourBasslinePitchMetric import ContourBasslinePitchMetric
from .ContourBasslineDurationMetric import ContourBasslineDurationMetric
from .ContourBasslineDurationQuantizedMetric import ContourBasslineDurationQuantizedMetric
from .ChromaticToneMetric import ChromaticToneMetric

class TestMetricsContoursAndChromatic(unittest.TestCase):
   """
   Test cases for Contours & Chromatic Metrics.
   """

   def setUp(self):
      """
      Set up test fixtures with a score designed to test melody and bassline contours.
      """
      self.score = Score("Test Score Contours")
      
      # Melody Part (Higher pitches)
      part1 = Part("Melody", PIANO, 0)
      phrase1 = Phrase(0.0)
      # Melody: C5, E5, G5, C6 (Ascending)
      phrase1.addNote(Note(C5, QN))
      phrase1.addNote(Note(E5, QN))
      phrase1.addNote(Note(G5, QN))
      phrase1.addNote(Note(C6, QN))
      part1.addPhrase(phrase1)
      self.score.addPart(part1)

      # Bassline Part (Lower pitches)
      part2 = Part("Bass", BASS, 1)
      phrase2 = Phrase(0.0)
      # Bass: C3, G2, C3, G2 (Alternating)
      phrase2.addNote(Note(C3, HN))
      phrase2.addNote(Note(G2, HN))
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
      
      self.assertIsNotNone(slope, f"{name} Slope should not be None")
      self.assertIsNotNone(r2, f"{name} R2 should not be None")

   def test_ContourMelodyPitchMetric(self):
      self.run_metric_test(ContourMelodyPitchMetric())

   def test_ContourMelodyDurationMetric(self):
      self.run_metric_test(ContourMelodyDurationMetric())

   def test_ContourMelodyDurationQuantizedMetric(self):
      self.run_metric_test(ContourMelodyDurationQuantizedMetric())

   def test_ContourBasslinePitchMetric(self):
      self.run_metric_test(ContourBasslinePitchMetric())

   def test_ContourBasslineDurationMetric(self):
      self.run_metric_test(ContourBasslineDurationMetric())

   def test_ContourBasslineDurationQuantizedMetric(self):
      self.run_metric_test(ContourBasslineDurationQuantizedMetric())

   def test_ChromaticToneMetric(self):
      self.run_metric_test(ChromaticToneMetric())

if __name__ == "__main__":
   unittest.main()
