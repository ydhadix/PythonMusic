# simpleTimer1.py
# Creates a Timer and prints a message every half second.

from timer import *

def test():
   print("It's ticking...")

t = Timer(500, test)
t.start()
