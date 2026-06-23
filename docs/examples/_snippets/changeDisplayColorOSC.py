# changeDisplayColorOSC.py
#
# It changes display color Continuously via OSC messages.
# It works with the TouchOSC Mk1 app (with accelerometer
# messages ("/accxyz") turned on).

from osc import *
from gui import *

# create OSC input object
oscIn = OscIn( 57110 )

# create display, whose color we will adjust
d = Display()

# function to call when an OSC "/accxyz" message arrives
def setDisplayColor(message):

   global d

   # get the message arguments - x, y, z
   args = message.getArguments()
   x = args[0]
   y = args[1]
   z = args[2]

   # NOTE: Based on the particular smartphone, x, y, z values
   # may range between -2.5 and 2.5.  So, use those values to set
   # the R G B values for the color.
   red   = mapValue(x, -2.5, 2.5, 0, 255)
   green = mapValue(y, -2.5, 2.5, 0, 255)
   blue  = mapValue(z, -2.5, 2.5, 0, 255)

   # create color
   color = Color(red, green, blue)

   # and set display color
   d.setColor( color )

# associate callback function with "/accxyz" messages
oscIn.onInput("/accxyz", setDisplayColor)
oscIn.hideMessages()