# simplePush.py
# Creates a Push and prints its value when it changes.

from gui import *

d = Display()

# function to specify what happens when button is pressed
def printValue(value):

   if value:        # if value is True, push is on
      print("Yes")  # replace this with whatever you want done when on

   else:            # else value is False (i.e., push is off)
      print("No")   # replace this with whatever you want done when off (if any)

t = Push(25, 25, 50, 50, printValue, Color.BLUE, Color.RED)
d.add(t)
