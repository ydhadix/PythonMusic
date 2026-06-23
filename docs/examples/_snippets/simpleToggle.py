# simpleToggle.py
# Creates a Toggle and prints its value when it changes.

from gui import *

d = Display()

# function to specify what happens when toggle is pressed
def printValue(value):

   if value:        # if value is True, push toggle is on
      print("Yes")  # replace this with whatever you want done when on

   else:            # else value is False (i.e., push toggle is off)
      print("No")   # replace this with whatever you want done when off (if any)

t = Toggle(25, 25, 50, 50, False, printValue, Color.WHITE, Color.BLACK, Color.RED, 1)
d.add(t)
