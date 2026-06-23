# RGB_Display.py
#
# Demonstrates how to use sliders to update values in real time (here, the
# background color of the display).  It also uses labels to provide additional
# feedback and visibility (by showing updated RGB values).
#

from gui import *

# create display
d = Display("RGB Display", 600, 400)

# initialize RGB values (0-255)
red   = 255
green = 255
blue  = 255

# initialize display background to these RGB values
d.setColor( Color(red, green, blue) )

# create labels for the sliders with black text and white background
labelRed   = Label(" R ", CENTER, Color.BLACK, Color.WHITE)
labelGreen = Label(" G ", CENTER, Color.BLACK, Color.WHITE)
labelBlue  = Label(" B ", CENTER, Color.BLACK, Color.WHITE)

# add labels to display
d.add(labelRed,   180, 132)
d.add(labelGreen, 180, 182)
d.add(labelBlue,  180, 232)

# create labels for the sliders' values with black text and white background
labelRedValue   = Label(" " + str(red) + " ",   CENTER, Color.BLACK, Color.WHITE)
labelGreenValue = Label(" " + str(green) + " ", CENTER, Color.BLACK, Color.WHITE)
labelBlueValue  = Label(" " + str(blue) + " ",  CENTER, Color.BLACK, Color.WHITE)

# add labels for values to display
d.add(labelRedValue,   400, 132)
d.add(labelGreenValue, 400, 182)
d.add(labelBlueValue,  400, 232)

# define function to update red value
def setRed(value):
   global d, red, green, blue, labelRedValue

   red = value                                 # update red value
   labelRedValue.setText(" " + str(red) + " ") # update red value label
   d.setColor(Color(red, green, blue))         # update background color

# define function to update green value
def setGreen(value):
   global d, red, green, blue, labelGreenValue

   green = value                                   # update green value
   labelGreenValue.setText(" " + str(green) + " ") # update green value label
   d.setColor(Color(red, green, blue))             # set background color

# define function to update blue value
def setBlue(value):
   global d, red, green, blue, labelBlueValue

   blue = value                                  # update blue value
   labelBlueValue.setText(" " + str(blue) + " ") # update blue value label
   d.setColor(Color(red, green, blue))           # set background color

# create sliders to set red, green, and blue values, respectively
sliderRed   = Slider(HORIZONTAL, 0, 255, red, setRed)
sliderGreen = Slider(HORIZONTAL, 0, 255, green, setGreen)
sliderBlue  = Slider(HORIZONTAL, 0, 255, blue, setBlue)

# add sliders to display
d.add(sliderRed,   200, 125)
d.add(sliderGreen, 200, 175)
d.add(sliderBlue,  200, 225)