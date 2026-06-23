from .data.PianoRoll import PianoRoll
from .metrics.ZipfMetrics import ZipfMetrics

# TODO: did the original call pianoroll without passing a quantum?
#       Dr. Manaris was remembering a possible bug with the original

class Surveyor:
   """
   (Definition: Surveyor -- someone who conducts a statistical (or other) survey.)

   Class Surveyor applies Metrics on music pieces.

   author Bill Manaris, Tim Hirzel, Patrick Roos
   version 04-01-2005
   """

   QUANTUM = 0.25    # default minimum note duration to be captured is 1/16th

   def survey(self, score, metrics, quantum=None):
      """
      Calculates all Metric's on the given score.

      param   score  a music Score to be evaluated (in)
      param   metrics  an array of Metric's to be applied to score (in/out)
      param   quantum  the width of a timeslice in the pianoroll representation (see PianoRoll)
      """
      if quantum is None:
         quantum = self.QUANTUM

      # perform sanity check... is the quantum within reasonable limits?
      # (Check commented out in Java original)

      # convert score to a piano roll representation
      pianoRoll = PianoRoll(score, quantum)

      # initialize each Metric
      fractalMetricsPresent = False
      for metric in metrics:
         metric.init()
         if metric.getType() == "Fractal":
            fractalMetricsPresent = True

      # Algorithm:  We will survey the piano roll linearly for simple metrics.
      # Then, if there are any fractal metrics we will also survey the piano roll recursively.

      # for simple metrics only linearly survey the complete piano roll
      self._surveyLinearly(metrics, pianoRoll)

      # for fractal metrics only recursively survey the complete piano roll
      if fractalMetricsPresent:
         self._surveyRecursively(metrics, pianoRoll, 0, pianoRoll.getLength() - 1)

   def _surveyLinearly(self, metrics, pianoRoll):
      """
      Linearly apply all Metric's on the given score.  Used for simple metrics.

      param   metrics - the list of Metric's to be used for surveying and collect measurements (in/out)
      param   pianoRoll - the pianoRoll to be surveyed (in)
      """
      # traverse the whole piano roll linearly rom left to right
      for timeSlice in range(pianoRoll.getLength()):
         for metric in metrics:    # iterate through all Metric's and measure current time slice
            if metric.getType() == "Simple":    # linear surveying is only for simple metrics
               metric.measureTimeSlice(pianoRoll, timeSlice)   # have current metric measure current time slice

      # NOTE: No metric merging is needed, since consecutive invocations of measureTimeSlice() have
      #       cummulative effect.

   def _surveyRecursively(self, metrics, pianoRoll, leftIndex, rightIndex):
      """
      Recursively apply all Metric's on the given score.  Used for fractal metrics.

      param   metrics - the list of Metric's to be used for surveying and collect measurements (in/out)
      param   pianoRoll - the pianoRoll to be surveyed (in)
      param   leftIndex - the index of the first slice to survey (in)
      param   rightIndex - the index of the last slice to survey (in)
      """
      if leftIndex == rightIndex:  # base case?
         for metric in metrics:    # iterate through all Metric's and measure current time slice
            if metric.getType() == "Fractal":    # recursive surveying is only for fractal metrics
               metric.measureTimeSlice(pianoRoll, leftIndex)
      else:                          # general case
         middleIndex = leftIndex + int((rightIndex - leftIndex) / 2)  # get middle index

         # Note: In Python, objects are passed by reference.
         # For fractal metrics, we need clean copies for the right subtree recursion
         # to avoid side effects before merging.

         leftMetrics = metrics
         rightMetrics = []

         for metric in leftMetrics:
            if metric.getType() == "Fractal":
               rightMetrics.append(metric.cloneHigherOrder())  # create a reinitialized copy
            else:
               rightMetrics.append(metric) # keep same metric for non-fractal (won't be used anyway)

         self._surveyRecursively(leftMetrics, pianoRoll, leftIndex, middleIndex)      # work on left subtree
         self._surveyRecursively(rightMetrics, pianoRoll, middleIndex + 1, rightIndex)  # work on right subtree

         boxSize = (rightIndex - leftIndex) + 1 # calculate box size of subtrees

         for i in range(len(metrics)):      # iterate through all Metric's and
            if leftMetrics[i].getType() == "Fractal":    # recursive surveying is only for fractal metrics
               leftMetrics[i].merge(rightMetrics[i], boxSize)  # ...merge their measurements
