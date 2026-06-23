# Animate a circle by moving it randomly.

from gui import *
from random import *
from timer import *

d = Display("Automation Example", 600, 400)

# initialize circle coordinates
x = 300
y = 200

# create filled red circle
c = Circle(x, y, 25, Color.RED, True)
d.add(c)

def moveCircle():

   global x, y   # these will be updated

   # update global circle coordinates
   x = x + randint(-5, 5)
   y = y + randint(-5, 5)

   # now, move circle
   d.move(c, x, y)

# start animation
Automate.add(moveCircle)
