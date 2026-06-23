# test_Histogram.py
#
# Unit tests for Histogram class.
#
# Usage:
#   python -m unittest src/nevmuse/data/test_Histogram.py

import os
import sys
import unittest

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from .Histogram import Histogram


class TestHistogram(unittest.TestCase):
   """
   Test cases for Histogram class.
   """

   def setUp(self):
      """
      Set up test fixtures.
      """
      self.hist = Histogram()

   def test_incrementCount_default(self):
      """Test incrementCount with default amount."""
      key = "testKey"
      self.hist.incrementCount(key)
      self.assertEqual(1.0, self.hist[key])

      self.hist.incrementCount(key)
      self.assertEqual(2.0, self.hist[key])

   def test_incrementCount_custom(self):
      """Test incrementCount with custom amount."""
      key = "testKey"
      self.hist.incrementCount(key, 2.5)
      self.assertEqual(2.5, self.hist[key])

      self.hist.incrementCount(key, 1.5)
      self.assertEqual(4.0, self.hist[key])

   def test_mergeCounts(self):
      """Test mergeCounts."""
      self.hist.incrementCount("A", 1.0)
      self.hist.incrementCount("B", 2.0)

      other = Histogram()
      other.incrementCount("B", 3.0)
      other.incrementCount("C", 4.0)

      self.hist.mergeCounts(other)

      self.assertEqual(1.0, self.hist["A"])
      self.assertEqual(5.0, self.hist["B"]) # 2.0 + 3.0
      self.assertEqual(4.0, self.hist["C"])

   def test_keysToDouble(self):
      """Test keysToDouble."""
      self.hist.incrementCount(1.0, 10.0)
      self.hist.incrementCount(2.5, 20.0)

      keys = self.hist.keysToDouble()
      keys.sort()

      self.assertEqual(2, len(keys))
      self.assertEqual(1.0, keys[0])
      self.assertEqual(2.5, keys[1])

   def test_valuesToDouble(self):
      """Test valuesToDouble."""
      self.hist.incrementCount("A", 1.5)
      self.hist.incrementCount("B", 2.5)

      values = self.hist.valuesToDouble()
      values.sort()

      self.assertEqual(2, len(values))
      self.assertEqual(1.5, values[0])
      self.assertEqual(2.5, values[1])


if __name__ == "__main__":
   unittest.main()
