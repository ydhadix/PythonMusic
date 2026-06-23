# iPianoSimple.py
#
# Demonstrates how to build a simple piano instrument playable
# through the computer keyboard.
#

from music import *
from gui import *

Play.setInstrument(PIANO)   # set desired MIDI instrument (0-127)

# load piano image and create display with appropriate size
pianoIcon = Icon("iPianoOctave.png")     # image for complete piano
display = Display("iPiano", pianoIcon.getWidth(),
                            pianoIcon.getHeight())
display.add(pianoIcon)       # place image at top-left corner

# load icons for pressed piano keys
cDownIcon      = Icon("iPianoWhiteLeftDown.png")    # C
cSharpDownIcon = Icon("iPianoBlackDown.png")        # C sharp
dDownIcon      = Icon("iPianoWhiteCenterDown.png")  # D
# ...continue loading icons for additional piano keys

# remember which keys are currently pressed
keysPressed = []

#####################################################################
# define callback functions
def beginNote(key):
   """This function will be called when a computer key is pressed.
      It starts the corresponding note, if the key is pressed for
      the first time (i.e., counteracts the key-repeat function of
      computer keyboards).
   """

   global display      # display surface to add icons
   global keysPressed  # list to remember which keys are pressed

   print("Key pressed is " + str(key))   # show which key was pressed

   if key == VK_Z and key not in keysPressed:
      display.add( cDownIcon, 0, 1 )  # "press" this piano key
      Play.noteOn( C4 )               # play corresponding note
      keysPressed.append( VK_Z )      # avoid key-repeat

   elif key == VK_S and key not in keysPressed:
      display.add( cSharpDownIcon, 45, 1 )  # "press" this piano key
      Play.noteOn( CS4 )                    # play corresponding note
      keysPressed.append( VK_S )            # avoid key-repeat

   elif key == VK_X and key not in keysPressed:
      display.add( dDownIcon, 76, 1 )  # "press" this piano key
      Play.noteOn( D4 )                # play corresponding note
      keysPressed.append( VK_X )       # avoid key-repeat

   # ...continue adding elif's for additional piano keys

def endNote(key):
   """This function will be called when a computer key is released.
      It stops the corresponding note.
   """

   global display      # display surface to add icons
   global keysPressed  # list to remember which keys are pressed

   if key == VK_Z:
      display.remove( cDownIcon )  # "release" this piano key
      Play.noteOff( C4 )           # stop corresponding note
      keysPressed.remove( VK_Z )   # and forget key

   elif key == VK_S:
      display.remove( cSharpDownIcon )  # "release" this piano key
      Play.noteOff( CS4 )               # stop corresponding note
      keysPressed.remove( VK_S )        # and forget key

   elif key == VK_X:
      display.remove( dDownIcon )  # "release" this piano key
      Play.noteOff( D4 )           # stop corresponding note
      keysPressed.remove( VK_X )   # and forget key

   # ...continue adding elif's for additional piano keys

#####################################################################
# associate callback functions with GUI events
display.onKeyDown( beginNote )
display.onKeyUp( endNote )