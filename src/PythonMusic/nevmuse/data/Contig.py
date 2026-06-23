"""
/**
 * A contig is a sub-section of the piano roll that contains
 * the same number of voices for each time-slice within the
 * sub-section.  Also, each voice in a contig is present in
 * every slice in the contig.  The voices, piano roll start
 * index, and piano roll end index are all retained within
 * the Contig object.
 */
"""


class Contig:
   """
   This class represents the splitting of the piano roll by voices. Each contig contains voices;
   every time the number of voices changes, a new contig is constructed. Each contig contains the
   voices in it as well as it's place in the piano roll.
   """

   def __init__(self, start, end, numberOfVoices):
      """
      Contig Constructor.

      param start: the start index of the pianoroll
      param end: the end index of the pianoroll
      param numberOfVoices: the number of voices in the contig, will be dynamically changing
      """
      # assign constructor arguments to instance variables
      self.start = start
      self.end = end
      self.voices = []
      self.voiced = False
      self.numberOfVoices = numberOfVoices   # store capacity (Python lists don't have capacity like Java Vectors)

   def getVoicesArray(self):
      """
      Returns the array of voices.

      return list[int]: the array of voices
      """
      return self.voices

   def numVoices(self):
      """
      Returns total number of voices or capacity of this contig if empty.

      return int: number of voices contig has been given if any, number of voices this contig can hold otherwise
      """
      if self.voiced:                   # If the contig has been voiced
         return len(self.voices)        # ...return number of voices contig has been given
      else:                             # ...else
         return self.numberOfVoices     # ...return number of voices this contig can hold

   def __str__(self):
      """
      Converts contig to string and returns that string.

      return str: string representation of this contig
      """
      voiced = "false"
      if self.voiced:
         voiced = "true"
      return "Voiced: " + voiced + "\nVoices: " + str(self.voices) + "\nStart: " + str(self.start) + " End: " + str(self.end)
