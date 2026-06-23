# simpleXYPad.py
# Creates an XYPad and prints its value when it changes

from gui import *

d = Display()

# function to specify what happens when tracker bubble is moved
def printPosition(x, y):
   print(x, y)  # replace this with whatever you want to do using x and y

trackpad = XYPad(100, 50, 200, 150, printPosition, Color.BLACK, Color.WHITE, Color.BLACK, 0)
d.add(trackpad)
