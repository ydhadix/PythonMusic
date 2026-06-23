# iPianoSimpleOSC.py
#
# Demonstrates how to build a simple piano instrument playable
# through the TouchOSC Mk1 app.
#

from music import *
from gui import *
from osc import *

Play.setInstrument(PIANO)   # set desired MIDI instrument (0-127)

# create OSC input
oscIn = OscIn()

# load piano image and create display with appropriate size
pianoIcon = Icon("iPianoOctave.png")     # image for complete piano
display   = Display("iPiano", pianoIcon.getWidth(),
                              pianoIcon.getHeight())
display.add(pianoIcon)       # place image at top-left corner

# load icons for pressed piano keys
cDownIcon      = Icon("iPianoWhiteLeftDown.png")    # C
cSharpDownIcon = Icon("iPianoBlackDown.png")        # C sharp
dDownIcon      = Icon("iPianoWhiteCenterDown.png")  # D
# ...continue loading icons for additional piano keys


#####################################################################
# define callback functions
def playNote(message):
   """This function is called when a message about an OSC piano key arrives.
      If the OSC piano key is being pressed, it starts the corresponding note.
      If the OSC piano key is released, it stops the corrsponding note.
   """

   global display      # display surface to add icons
   global cDownIcon, cSharpDownIcon, dDownIcon

   # retrieve address and arguments
   address   = message.getAddress()
   arguments = message.getArguments()

   # now, get first argument (it may be 1.0 which means pressed, or 0.0 which
   # means unpressed)
   value = arguments[0]

   # is it the C key?
   if address ==  "/1/push1":

      # yes, so check if piano key is being pressed or unpressed
      if value == 1.0:   # is it being pressed?

         display.add( cDownIcon, 0, 1 )   # "press" this piano key
         Play.noteOn( C4 )                # play corresponding note

      else:   # it is being unpressed (value is 0.0)

         display.remove( cDownIcon )  # "release" this piano key
         Play.noteOff( C4 )           # stop corresponding note

   # is it the C# key?
   elif address ==  "/1/push2":

      # yes, so check if piano key is being pressed or unpressed
      if value == 1.0:   # is it being pressed?

         display.add( cSharpDownIcon, 45, 1 )   # "press" this piano key
         Play.noteOn( CS4 )                     # play corresponding note

      else:   # it is being unpressed (value is 0.0)

         display.remove( cSharpDownIcon )   # "release" this piano key
         Play.noteOff( CS4 )                # stop corresponding note

   # is it the D key?
   elif address ==  "/1/push3":

      # yes, so check if piano key is being pressed or unpressed
      if value == 1.0:   # is it being pressed?

         display.add( dDownIcon, 76, 1 )   # "press" this piano key
         Play.noteOn( D4 )                 # play corresponding note

      else:   # it is being unpressed (value is 0.0)

         display.remove( dDownIcon )   # "release" this piano key
         Play.noteOff( D4 )            # stop corresponding note

   # ...continue adding elif's for additional piano keys


#####################################################################
# associate callback function with OSC messages
#oscIn.onInput( ".*", playNote )         # for all incoming OSC addresses
oscIn.onInput( "/1/push.*", playNote )   # only for addresses starting with "/1/push" !!!

oscIn.hideMessages()