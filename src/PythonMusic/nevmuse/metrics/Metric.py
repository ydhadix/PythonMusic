from abc import ABC, abstractmethod
from collections import deque
import zipf
from ..data.Histogram import Histogram
from ..data.Measurement import Measurement
from .ZipfMetrics import ZipfMetrics

class Metric(ABC):
   """
   (Definition: Metric -- a system of related measures that facilitates
   the quantification of some particular music attribute.)

   It encapsulates the process of deriving measures (objects of class Measurement)
   for power-law metrics.

   author Bill Manaris, Luca Pellicoro, Patrick Roos
   version 1.3 (February 24, 2007)
   """

   def __init__(self, name, typeInt, distribution, level, numHigherOrder):
      """
      It constructs a metric with the specified name, type, distribution, and number of higher-order levels.

      param name  the name of the metric (e.g., "Pitch")
      param typeInt  the type of the metric (e.g., SIMPLE or FRACTAL)
      param distribution  the distribution of the metric (e.g., BY_RANK or BY_SIZE)
      param level the high-order level of the current metric (0 means base metric)
      param numHigherOrder the number of higher-order distributions to calculate (0 means only base metric)
      """
      assert typeInt == ZipfMetrics.SIMPLE or typeInt == ZipfMetrics.FRACTAL, \
         f"Type must be either SIMPLE ({ZipfMetrics.SIMPLE}), or FRACTAL ({ZipfMetrics.FRACTAL}), instead it was ({typeInt})"

      assert distribution == ZipfMetrics.BY_RANK or distribution == ZipfMetrics.BY_SIZE, \
         f"Distribution must be either BY_RANK ({ZipfMetrics.BY_RANK}), or BY_SIZE ({ZipfMetrics.BY_SIZE}), instead it was ({distribution})"

      assert level <= numHigherOrder, \
         f"Level cannot be higher than number of higher-order metrics ({level}, {numHigherOrder})"

      assert numHigherOrder >= 0, \
         f"Number of higher-order metrics must by non-negative ({numHigherOrder})"

      self.name = name
      self.type = typeInt
      self.distribution = distribution
      self.level = level
      self.numHigherOrder = numHigherOrder

      self.histogram = Histogram()

      # for local variability
      self.queue = deque()
      self.localVariabilityHistogram = Histogram()

      # build the list of metrics
      if self.level >= self.numHigherOrder:
         self.higherOrder = None      # no higher-order metrics
      else:
         self.higherOrder = self.cloneHigherOrder()   # construct the remaining metrics (recursively)

   @abstractmethod
   def cloneHigherOrder(self):
      """
      Should be defined to return a new instance of the Metric.
      """
      pass

   @abstractmethod
   def measureTimeSlice(self, pianoRoll, timeIndex):
      """
      Should be defined to count the events of interest found in the specified time slice of
      the piano roll.

      param  pianoRoll  a Piano Roll representation of a Score
      param  noteIndex   the index of the current time slice within the piano roll
      """
      pass

   def init(self):
      """
      It initializes the metric's internal data structure.
      It recursively initializes all higher-order metrics.
      """
      self.histogram.clear()
      self.queue.clear()
      self.localVariabilityHistogram.clear()

      if self.higherOrder is not None: # do we have more metrics to clear?
         self.higherOrder.init()

   def removeHigherOrderLastEvents(self):
      """
      It resets the metric's higher-order metrics by removing "last event" histograms entries
      (used to calculate higher-order metrics).  It keeps histogram counts as they are.
      """
      if "last event" in self.histogram:
         del self.histogram["last event"]

      if self.higherOrder is not None: # do we have more metrics to work on?
         self.higherOrder.removeHigherOrderLastEvents()

   def count(self, event):
      """
      This recursive method will increment counts on all the histograms.
      """
      # Base case: either were are the last higher-order metric, or this is a fresh histogram
      if self.higherOrder is None or "last event" not in self.histogram:
         self.histogram["last event"] = event
         if not (self.distribution == ZipfMetrics.BY_SIZE and event == 0.0):
            self.histogram.incrementCount(event)
      else:
         # store the count
         if not (self.distribution == ZipfMetrics.BY_SIZE and event == 0.0):
            self.histogram.incrementCount(event)

         # calculate the difference
         change = event - self.histogram["last event"]

         # remember the latest event
         self.histogram["last event"] = event

         if self.distribution == ZipfMetrics.BY_SIZE:
            change = abs(change)

         # count the change as a higher-order event
         self.higherOrder.count(change)

      # also count the local variability of this event
      self.countLocalVariability(event)

   def countLocalVariability(self, event):
      """
      Calculates and counts local variability for an event.
      """
      self.queue.append(event)  # add event to the end of the queue

      if len(self.queue) == 5: # do we have enough events in the window?
         # calculate local variability of event
         localAvg = self._getLocalAvg()

         # NOTE: Handling potential division by zero if localAvg is 0
         if localAvg != 0:
            localVar = abs((event - localAvg) / localAvg)
            # count local variability of event to the local variability histogram
            self.localVariabilityHistogram.incrementCount(localVar)

         # now, remove the first event in the window
         self.queue.popleft()

   def _getLocalAvg(self):
      """
      Returns the average of the events in this.queue
      """
      # check precondition using assertion
      assert len(self.queue) == 5

      sum_val = sum(self.queue)
      avg = sum_val / len(self.queue)

      return avg

   def getMeasurement(self):
      """
      Will collect all the measurements from the recursively defined chain of higher-order Metric objects.
      """
      assert self.distribution == ZipfMetrics.BY_RANK or self.distribution == ZipfMetrics.BY_SIZE, \
         f"Distribution must be either BY_RANK ({ZipfMetrics.BY_RANK}), or BY_SIZE ({ZipfMetrics.BY_SIZE}), instead it was ({self.distribution})"

      if self.higherOrder is None:
         result = Measurement(self.name, self.distribution, self.level)
         return self._extractMeasurement(result)
      else:
         result = self.higherOrder.getMeasurement()
         return self._extractMeasurement(result)

   def _extractMeasurement(self, result):
      if "last event" in self.histogram:
         del self.histogram["last event"]

      if self.distribution == ZipfMetrics.BY_RANK:
         self._addMeasurementByRank(result, self.histogram, self.level)
      else: # assume BY_SIZE
         self._addMeasurementBySize(result, self.histogram, self.level)

      self._addLocalVariabilityMeasurement(result, self.localVariabilityHistogram, self.level)

      return result

   def _addMeasurementByRank(self, measurement, histogram, level):
      """
      Calculates rank-frequency distribution slope and R^2.
      """
      values = histogram.valuesToDouble()
      if not values:
         slope, r2 = 0.0, 0.0
      else:
         # zipf.byRank returns (slope, r2, yint)
         slope, r2, _ = zipf.byRank(values)

      # retrieve the slope and R^2 values and store them in 'measurement'
      measurement.add(level, "", "slope", slope)
      measurement.add(level, "", "r2", r2)

   def _addMeasurementBySize(self, measurement, histogram, level):
      """
      Calculates size-frequency distribution slope and R^2.
      """
      keys = histogram.keysToDouble()
      values = histogram.valuesToDouble()
      if not keys or not values:
         slope, r2 = 0.0, 0.0
      else:
         # zipf.bySize returns (slope, r2, yint)
         slope, r2, _ = zipf.bySize(keys, values)

      # retrieve the slope and R^2 values and store them in 'measurement'
      measurement.add(level, "", "slope", slope)
      measurement.add(level, "", "r2", r2)

   def _addLocalVariabilityMeasurement(self, measurement, histogram, level):
      """
      Calculates rank-frequency distribution slope and R^2 for local variability.
      """
      values = histogram.valuesToDouble()

      if not values:
         slope, r2 = 0.0, 0.0
      else:
         slope, r2, _ = zipf.byRank(values)

      measurement.add(level, "_LocalVariability", "slope", slope)
      measurement.add(level, "_LocalVariability", "r2", r2)
   def merge(self, otherMetric, boxSize):
      """
      It merges the internal data structure of otherMetric into this Metric.
      """
      assert self.name == otherMetric.name, \
         f"The two metrics should have the same name; those provided where {self.name} and {otherMetric.name}"

      assert self.type == otherMetric.type, \
         f"The two metrics should be of the same type; those provided had type {self.type} and {otherMetric.type}"

      assert self.distribution == otherMetric.distribution, \
         f"The two metrics should be of the same distribution type; those provided had distribution type {self.distribution} and {otherMetric.distribution}"

      assert self.numHigherOrder == otherMetric.numHigherOrder, \
         f"The two metrics should have the same number of levels; those provided have levels {self.numHigherOrder} and {otherMetric.numHigherOrder}!"

      # merge corresponding histograms
      self.histogram.mergeCounts(otherMetric.histogram)
      self.localVariabilityHistogram.mergeCounts(otherMetric.localVariabilityHistogram)

      if self.higherOrder is not None: # do we have more metrics to work on?
         self.higherOrder.merge(otherMetric.higherOrder, boxSize)

   def getName(self):
      return self.name

   def getType(self):
      result = ""

      assert self.type == ZipfMetrics.SIMPLE or self.type == ZipfMetrics.FRACTAL, \
         f"Type must be either SIMPLE ({ZipfMetrics.SIMPLE}), or FRACTAL ({ZipfMetrics.FRACTAL}), instead it was ({self.type})"

      if self.type == ZipfMetrics.SIMPLE:
         result = "Simple"
      elif self.type == ZipfMetrics.FRACTAL:
         result = "Fractal"

      return result

   def getDistribution(self):
      result = ""

      assert self.distribution == ZipfMetrics.BY_RANK or self.distribution == ZipfMetrics.BY_SIZE, \
         f"Distribution must be either BY_RANK ({ZipfMetrics.BY_RANK}), or BY_SIZE ({ZipfMetrics.BY_SIZE}), instead it was ({self.distribution})"

      if self.distribution == ZipfMetrics.BY_RANK:
         result = "by Rank"
      elif self.distribution == ZipfMetrics.BY_SIZE:
         result = "by Size"

      return result

   def getHigherOrderCount(self):
      return self.numHigherOrder

   def __str__(self):
      result = f"Name: {self.name}\n"
      result += f"Type: {self.getType()}\n"
      result += f"Distribution: {self.getDistribution()}\n"
      result += f"HigherOrderCount: {self.getHigherOrderCount()}\n"

      return self.toStringHelper(result)

   def toStringHelper(self, result):
      # Recursive logic to build string chain
      current = f"Histogram Order: {self.level} {str(self.histogram)}\n"

      # NOTE: In the original Java, it seemed to duplicate previous string.
      # Here we append current part to result and recurse.
      result += current

      if self.higherOrder is not None:
         return self.higherOrder.toStringHelper(result)

      return result
