import random
import math

class PowerLawRandom(random.Random):
   """
   This class can be used to create random number generators whose values are
   in the range >=0 to MAX_VALUE and follow a desired power-law distribution.
   It uses Python's random module to obtain uniformly-distributed random numbers, which it
   then maps to numbers with the desired distribution.

   author Bill Manaris (with feedback from Tim Hirzel)
   version 1.1  May 29, 2004
   """

   MAX_VALUE = 32767  # Short.MAX_VALUE in Java

   def __init__(self, power=1.0, seed=None, max_val=None):
      """
      Creates a power-law number generator.

      param power: power of random number distribution (power-law slope is approx. -power).
      param seed: seed for random number generator.
      param max_val: max upper range (default Short.MAX_VALUE).
      """
      super().__init__(seed)
      self.power = power
      self.rcpPower = 1.0 / self.power
      self.MAX_VALUE = max_val if max_val is not None else 32767

   def nextBoolean(self):
      """
      Returns random boolean with specified distribution.
      """
      return self.randint(0, 1) == 1

   def nextLong(self):
      """
      Returns random long >=0 and < MAX_VALUE with specified distribution.
      """
      return self.nextInt(self.MAX_VALUE)

   def nextInt(self, max_val=None):
      """
      Returns random int >= 0 and < max_val with specified distribution.
      If max_val is None, uses self.MAX_VALUE.

      param max_val: upper limit of the range (must be > 0 and <= MAX_VALUE)
      """
      if max_val is None:
         max_val = self.MAX_VALUE

      # ensure that max is positive
      if max_val <= 0:
         raise ValueError("max_val must be positive")

      # ensure that max is not too large
      if max_val > self.MAX_VALUE:
         raise ValueError(f"max_val must be less than PowerLawRandom.MAX_VALUE ({self.MAX_VALUE})")

      # get a random value >= 0 and < max_val using uniform distribution from super
      # In Java: super.nextInt() returns full range int, then % max.
      # Python's random.randint(a, b) includes endpoints. random.randrange(stop) excludes stop.
      # To mimic super.nextInt() % max behavior (uniform random):
      value = super().randrange(max_val)

      # finds the subrange within which 'value' is included
      isRanked = False           # have not yet found the propoer rank window
      denominator = 1.0          # initialize denominator of power function
      rank = 1.0                 # initialize rank for this denominator

      while not isRanked and rank < max_val:
         if value < max_val - (max_val / denominator):
            isRanked = True # done
         else:
            rank += 1.0          # get the next denominator of the power function
            denominator = math.pow(rank, self.rcpPower)

      # now, we have found the subrange (rank) within which 'value' is included...
      # rank, by definition, has probability of occurrence given by our power-law distribution.

      return int(rank - 1)   # returns random int >= 0 and < max with specified distribution

   def nextFloat(self):
      """
      Returns random float >=0.0 and < 1.0 with specified distribution.
      """
      return float(self.nextDouble())

   def nextDouble(self):
      """
      Returns random double >=0.0 and < 1.0 with specified distribution.
      """
      # map the int random value to the range >=0.0 and < 1.0
      return float(self.nextInt(self.MAX_VALUE)) / float(self.MAX_VALUE)

if __name__ == "__main__":
   # Simple test matching the Java main method logic
   powerLaw1 = PowerLawRandom(0.1, 100, 10000)
   print("Testing PowerLawRandom...")
   for _ in range(10):
      print(powerLaw1.nextInt())
