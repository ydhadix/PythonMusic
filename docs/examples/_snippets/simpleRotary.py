# simpleRotary.py
# Creates a Rotary and prints its value when it changes.

from gui import *

d = Display()

# function to specify what happens when knob is turned
def printValue(value):
   print(value)   # replace this with whatever needs to happen

knob = Rotary(5, 5, 100, 100, -100, 100, 0, printValue, Color.WHITE, Color.BLACK, Color.RED, 1, 300)

d.add(knob)