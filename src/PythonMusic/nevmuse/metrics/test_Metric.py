# test_Metric.py
#
# Unit tests for Metric abstract base class.
#
# Usage:
#   python -m unittest src/nevmuse/metrics/test_Metric.py

import os
import sys
import unittest
from .Metric import Metric
from .ZipfMetrics import ZipfMetrics

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

class MockMetric(Metric):
   """
   Concrete implementation of Metric for testing purposes.
   """
   def cloneHigherOrder(self):
      return MockMetric(self.name, self.type, self.distribution, self.level + 1, self.numHigherOrder)

   def measureTimeSlice(self, pianoRoll, timeIndex):
      pass # Not needed for these tests

class TestMetric(unittest.TestCase):
   """
   Test cases for Metric class.
   """

   def setUp(self):
      """
      Set up test fixtures.
      """
      self.metric = MockMetric("TestMetric", ZipfMetrics.SIMPLE, ZipfMetrics.BY_RANK, 0, 1)

   def test_initialization(self):
      """Test proper initialization and recursive creation."""
      self.assertEqual("TestMetric", self.metric.getName())
      self.assertEqual("Simple", self.metric.getType())
      self.assertEqual("by Rank", self.metric.getDistribution())
      self.assertEqual(1, self.metric.getHigherOrderCount())
      
      # Check higher order
      self.assertIsNotNone(self.metric.higherOrder)
      self.assertEqual(1, self.metric.higherOrder.level)
      self.assertIsNone(self.metric.higherOrder.higherOrder) # Last one

   def test_count_recursion(self):
      """Test that count propagates to higher orders."""
      # Level 0: [10.0, 20.0, 30.0]
      # Level 1 (Diff): [10.0, 10.0]
      
      self.metric.count(10.0)
      self.metric.count(20.0)
      self.metric.count(30.0)
      
      # Check Level 0
      # last event should be 30.0
      self.assertEqual(30.0, self.metric.histogram["last event"])
      # counts: 10, 20, 30 each once
      self.assertEqual(1.0, self.metric.histogram.get(10.0))
      self.assertEqual(1.0, self.metric.histogram.get(20.0))
      self.assertEqual(1.0, self.metric.histogram.get(30.0))
      
      # Check Level 1 (Higher Order)
      # differences: 20-10=10, 30-20=10.
      # So 10.0 should have count 2.
      ho = self.metric.higherOrder
      self.assertEqual(2.0, ho.histogram.get(10.0))
      self.assertEqual(10.0, ho.histogram["last event"])

   def test_local_variability(self):
      """Test local variability calculation."""
      # Window size 5. First 4 don't generate stats.
      # Data: [10, 10, 10, 10, 10] -> Avg=10. Variability=0.
      
      for _ in range(5):
         self.metric.count(10.0)
         
      # The 5th event should trigger calculation.
      # LocalVar = |10 - 10| / 10 = 0.
      self.assertEqual(1.0, self.metric.localVariabilityHistogram.get(0.0))
      
      # Add 6th event: 20.
      # Window: [10, 10, 10, 10, 20]. Sum=60. Avg=12.
      # LocalVar = |20 - 12| / 12 = 8/12 = 2/3 approx 0.666...
      self.metric.count(20.0)
      
      # Check if key exists near 0.666
      keys = self.metric.localVariabilityHistogram.keys()
      found = False
      for k in keys:
         if abs(k - 0.666666) < 0.001:
            found = True
            break
      self.assertTrue(found)

   def test_getMeasurement(self):
      """Test retrieving measurement."""
      # Add some data
      for i in range(10):
         self.metric.count(float(i))
         
      m = self.metric.getMeasurement()
      
      # Should contain keys for level 0 and 1
      # keys like TestMetric_0_Slope, TestMetric_1_Slope
      
      self.assertIsNotNone(m.get("TestMetric_0_Slope"))
      self.assertIsNotNone(m.get("TestMetric_1_Slope"))

if __name__ == "__main__":
   unittest.main()
