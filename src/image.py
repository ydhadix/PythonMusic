#######################################################################################
# image.py       Version 1.6     30-Jan-2025
#
# Taj Ballinger, Trevor Ritchie, and Bill Manaris
#
# Deprecated - kept for backwards compatibility.
#######################################################################################
#
# This file is part of PythonMusic.
#
# PythonMusic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PythonMusic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PythonMusic.  If not, see <https://www.gnu.org/licenses/>.
#
# PythonMusic derives from JythonMusic (https://jythonmusic.me),
# Copyright (C) 2011-2023 Bill Manaris, John-Anthony Thevos, Marge Marshall,
# Chris Benson, and Kenneth Hanson.
# Modifications Copyright (C) 2025 Dr. Bill Manaris and the PythonMusic contributors.
#######################################################################################
#
# REVISIONS:
#
# 1.6   30-Jan-2025 (tb)   Ported from JythonMusic to PythonMusic.
#      - Deprecated; Reduced to compatibility shim wrapping Display and Icon
#
#######################################################################################

from gui import Display, Icon
from utilities import *    # mapValue, etc.

class Image:
   """Show and edit an image, pixel by pixel or as a whole.

   This module is deprecated and kept only for backwards compatibility. For new code, use
   Display and Icon from the gui library instead.

   Create an Image in a few ways:
   - Image(filename) loads an image from a file.
   - Image(filename, width) loads an image and scales it to that width.
   - Image(width) makes a blank square canvas that many pixels wide.
   - Image(width, height) makes a blank canvas of that width and height.

   Store the result in a variable, for example img = Image("sunset.jpg"). Pixels are read
   and written by column and row, with the top-left pixel at (0, 0).

   Args:
       arg1 (str or int): A filename to load, or the width of a blank canvas, in pixels.
       arg2 (int, optional): A width to scale the loaded image to, or the height of a blank canvas, in pixels.
   """
   def __init__(self, arg1, arg2=None):
      # JythonMusic's Image class has overloaded constructors,
      # but Python doesn't allow that.  We replicate an overload based on the
      # data types of arg1 and arg2.
      #
      # (str, None) -> a filename for an image to load
      # (str, int)  -> a filename for an image to load, scaled to a width
      # (int, None) -> the width of a square, blank canvas
      # (int, int)  -> the width and height of a blank canvas

      self._display = Display()  # the display the image is on
      self._icon    = None       # the icon that holds the image data (created in read())
      self.read(arg1, arg2)      # read() loads the icon and sets Display properties

   def show(self):
      """Show the image in its window.
      """
      self._display.show()

   def hide(self):
      """Hide the image's window.

      Use show() to bring the window back.
      """
      self._display.hide()

   def getWidth(self):
      """Return the image's width.

      Returns:
          width (int): The width, in pixels.
      """
      return self._display.getWidth()

   def getHeight(self):
      """Return the image's height.

      Returns:
          height (int): The height, in pixels.
      """
      return self._display.getHeight()

   # pixel manipulation wrappers

   def getPixel(self, col, row):
      """Return the color of one pixel.

      The top-left pixel is at (0, 0).

      Args:
          col (int): The pixel's column (its horizontal position in the image).
          row (int): The pixel's row (its vertical position in the image).

      Returns:
          pixel (list[int]): The pixel's red, green, and blue values, for example [255, 0, 0].
      """
      return self._icon.getPixel(col, row)

   def setPixel(self, col, row, RGBList):
      """Set the color of one pixel.

      The top-left pixel is at (0, 0).

      Args:
          col (int): The pixel's column (its horizontal position in the image).
          row (int): The pixel's row (its vertical position in the image).
          RGBList (list[int]): The new red, green, and blue values, for example [255, 0, 0].
      """
      self._icon.setPixel(col, row, RGBList)

   def getPixels(self):
      """Return every pixel in the image.

      The pixels are arranged as a list of rows, each row a list of pixels, each pixel a list
      of red, green, and blue values. The image's top-left pixel is at [0][0].

      Returns:
          pixelList (list[list[list[int]]]): The image's pixels, by row then column, each as [red, green, blue].
      """
      return self._icon.getPixels()

   def setPixels(self, pixels):
      """Replace every pixel in the image.

      The pixels are arranged as a list of rows, each row a list of pixels, each pixel a list
      of red, green, and blue values. The image's top-left pixel is at [0][0].

      Args:
          pixels (list[list[list[int]]]): The new pixels, by row then column, each as [red, green, blue].
      """
      self._icon.setPixels(pixels)

   def save(self, filename):
      """Save the image to a file.

      Args:
          filename (str): The file to write, ending in ".jpg" or ".png".
      """
      self._display.save(filename)

   def write(self, filename):
      """Save the image to a file.

      Same as save().

      Args:
          filename (str): The file to write, ending in ".jpg" or ".png".
      """
      self.save(filename)

   def read(self, arg1, arg2=None):
      """Load new content into the image, replacing what it held.

      Takes the same forms as creating an Image: a filename (with an optional width to scale
      to), or a width (with an optional height) for a blank canvas.

      Args:
          arg1 (str or int): A filename to load, or the width of a blank canvas, in pixels.
          arg2 (int, optional): A width to scale the loaded image to, or the height of a blank canvas, in pixels.
      """
      # first, load the icon
      if isinstance(arg1, str):
         # arg1 is a filename
         title = arg1
         icon  = Icon(arg1, arg2)  # load icon with optional resizing
      else:
         # arg1 is a image size
         title = "Image"
         icon  = Icon("", arg1, arg2)  # load blank icon, sized to given dimensions

      # remove the previous icon, if needed
      if self._icon is not None:
         self._display.remove(self._icon)

      # next, update the Display
      width, height = icon.getSize()
      self._display.setSize(width, height)
      self._display.setTitle(title)

      # finally, add new icon to the display
      self._icon = icon
      self._display.add(icon)


#######################################################################################
# Tests
#######################################################################################

if __name__ == "__main__":
   pass
