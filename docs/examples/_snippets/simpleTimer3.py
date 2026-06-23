# simpleTimer3.py
# Creates a Timer to move a circle every half second.

from gui import *
from timer import *

d = Display()

# create a circle to move
c = Circle(50, 50, 30, Color.RED, True)
d.add(c)

# function to move circle a number of pixels on the diagonal,
# when called
def moveCircle(incrementX, incrementY):

   global d, c

   x = c.getX()
   y = c.getY()

   d.move(c, x + incrementX, y + incrementY)

# create timer to call move function every 0.5 sec
parameters = [5, 5]
t = Timer(500, moveCircle, parameters, True)
t.start()   # and start it!!
