
class Histogram(dict):
   """
   This class encapsulates components of histograms maintained by metrics.
   It is a superset for class Hashtable.  A Histogram consists of keys (of class
   Object) and values (always of class Double).

   author Bill Manaris and Brian Murtagh
   version 1.1, July 29, 2005 (simplified code, Bill Manaris)
   version 1.0, June 2, 2005

   see java.util.Hashtable
   """

   def incrementCount(self, key, amount=1.0):
      """
      Increments the value associated with the provided key in this Histogram.
      If the key does not exist, a new key-value pair is introduced.

      param key     the key whose value is to be incremented
      param amount  the amount by which to increment the key's value (defaults to 1.0)
      """
      # Note: For efficiency, we should change 'amount' to double, and create an Double object only when put() is called.
      if key in self:   # have we seen it before?
         value = self[key]   # get the old value
         value += amount     # increment it
         self[key] = value   # put it back into the histogram
      else:
         self[key] = amount  # this key does not exist, so introduce it

   def mergeCounts(self, otherHistogram):
      """
      For each of the keys in otherHistogram it adds their values with the corresponding key in this Histogram.
      If a key does not exist, a new key-value pair is introduced in this Histogram.

      Note:  It assumes all values are of type Double

      param otherHistogram  the histogram whose values are to be added to ours
      """
      # iterate through all keys in otherHistogram
      for otherKey, otherValue in otherHistogram.items():
         self.incrementCount(otherKey, otherValue) # yes, so add its value to ours

         #System.out.println("key: " + otherKey + "= value: " + this.get(otherKey) );

   def keysToDouble(self):
      """
      Returns a double array of the Histogram keys.
      """
      # iterate through all keys in the Histogram
      keys = []
      for key in self.keys():
         keys.append(float(key))   # convert it to double and store it in the array

      return keys

   def valuesToDouble(self):
      """
      Returns a double array of the Histogram values.
      """
      # iterate through all values in the Histogram
      values = []
      for value in self.values():
         values.append(float(value))  # convert it to double and store it in the array

      return values
