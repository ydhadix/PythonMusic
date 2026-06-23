# simpleFader.py
# Creates a VFader and prints its value when it changes.

from gui import *

d = Display()

# function to specify what happens when fader is moved
def printValue(value):
   print(value)   # replace this with whatever action needs to happen

fader = VFader(25, 5, 45, 80, 0, 100, 50, printValue)
d.add(fader)
