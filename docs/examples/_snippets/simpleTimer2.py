# simpleTimer2.py
# Creates a Timer and plays an A4 note every half second.

from timer import *
from music import *

t = Timer(500, Play.noteOn, [A4], True)
t.start()
