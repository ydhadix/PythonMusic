#######################################################################################
# utilities.py       Version 1.0     22-Jun-2026
#
# Taj Ballinger and Bill Manaris
#
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
# 1.0   22-Jun-2026 (tb)   New module consolidating helpers from JythonMusic music and animate.
#      - Holds value-mapping and float-range helpers (map, mapValue, mapScale, frange, xfrange)
#      - Imported by every library, so available without explicit import
#
#######################################################################################
# 
# A collection of useful, library-agnostic PythonMusic functions.
# 

#######################################################################################
# Mapping Values
#######################################################################################

def map(value, minValue, maxValue, minResult, maxResult):
   """Convert a number from one range to another, including values outside the source range.

   For example, 5 in the range 0 to 10 maps to 50 in the range 0 to 100. The number may
   lie outside the source range: it is then carried just as far outside the destination
   range (for example, 15 in the range 0 to 10 maps to 150 in the range 0 to 100). To
   require the number to stay within the source range instead, use mapValue().

   Args:
       value (int or float): The number to convert.
       minValue (int or float): The low end of the source range (inclusive).
       maxValue (int or float): The high end of the source range (inclusive).
       minResult (int or float): The low end of the destination range (inclusive).
       maxResult (int or float): The high end of the destination range (inclusive).

   Returns:
       mappedValue (int or float): The number's matching place relative to the destination range. It is an int if minResult is an int, otherwise a float.
   """
   value = float(value)  # ensure float division for accuracy
   
   normal = (value - minValue) / (maxValue - minValue)         # normalize to first range...
   mappedValue = minResult + (maxResult - minResult) * normal  # ... and lerp to second range
   
   destinationType = type(minResult)  # match the destination's data type
   mappedValue = destinationType(mappedValue)

   return mappedValue


def mapValue(value, minValue, maxValue, minResult, maxResult):
   """Convert a number from one range to its matching place in another range.

   For example, 5 in the range 0 to 10 maps to 50 in the range 0 to 100. The number must
   lie within the source range; to allow numbers outside it, use map() instead.

   Args:
       value (int or float): The number to convert; it must be between minValue and maxValue.
       minValue (int or float): The low end of the source range (inclusive).
       maxValue (int or float): The high end of the source range (inclusive).
       minResult (int or float): The low end of the destination range (inclusive).
       maxResult (int or float): The high end of the destination range (inclusive).

   Returns:
       mappedValue (int or float): The number's matching place in the destination range. It is an int if minResult is an int, otherwise a float.
   """
   # a value outside the source range cannot be mapped; use map() to allow that
   if value < minValue or value > maxValue:
      raise ValueError(f"mapValue(): value '{value}' is outside the specified range ('{minValue}' to '{maxValue}').")

   mappedValue = map(value, minValue, maxValue, minResult, maxResult)
   return mappedValue


def mapScale(value, minValue, maxValue, minResult, maxResult, scale=None, key=None):
   """Map a number from one range to another, snapped to a musical scale.

   Works like mapValue(), but rounds the result to the nearest pitch in the given
   scale, so the output is always a usable MIDI pitch. A scale is a list of pitch
   classes between 0 and 11 (see the scale constants such as MAJOR_SCALE). The key is
   the scale's root pitch class, where 0 means C, 1 means C#/Db, … 11 means B; if it is
   left out, the key is taken from minResult.

   Args:
       value (int or float): The number to map.
       minValue (int or float): The lowest number value can take (inclusive).
       maxValue (int or float): The highest number value can take (inclusive).
       minResult (int or float): The lowest pitch of the destination range (inclusive).
       maxResult (int or float): The highest pitch of the destination range (inclusive).
       scale (list[int], optional): The scale to snap to, a list of pitch classes between 0 and 11. If omitted, every pitch is allowed (the chromatic scale).
       key (int, optional): The scale's root pitch class, from 0 to 11. If omitted, it is taken from minResult.

   Returns:
       mappedPitch (int): The mapped number, snapped to the scale, as a MIDI pitch.
   """
   # check if value is within the specified range
   if value < minValue or value > maxValue:
      raise ValueError("value, " + str(value) + ", is outside the specified range, " \
                                 + str(minValue) + " to " + str(maxValue) + ".")

   # replace scale with chromatic scale if not provided
   if scale is None:
      scale = list(range(12))  # manual CHROMATIC_SCALE to avoid importing music.py

   # clamp value to specified range
   value = min(maxValue, max(value, minValue))

   # check pitch row - it should contain offsets only from 0 to 11
   badOffsets = [offset for offset in scale if offset < 0 or offset > 11]
   if badOffsets != []:  # any illegal offsets?
      raise TypeError("scale, " + str(scale) + ", should contain values only from 0 to 11.")

   # figure out key of scale
   if key is None:           # if they didn't specify a key
      key = minResult % 12   # assume that minResult the root of the scale
   else:                     # otherwise,
      key = key % 12         # ensure it is between 0 and 11 (i.e., C4 and C5 both mean C, or 0).

   # we are OK, so let's map
   value = float(value)  # ensure we are using float (for accuracy)
   normal = (value - minValue) / (maxValue - minValue)   # normalize source value

   # map to destination range (i.e., chromatic scale)
   # (subtracting 'key' aligns us with indices in the provided scale - we need to add it back later)
   chromaticStep = normal * (maxResult - minResult) + minResult - key

   # map to provided scale
   pitchRowStep = chromaticStep * len(scale) / 12   # position within scale
   pitchRowStep = round(pitchRowStep)               # snap to the nearest scale degree

   scaleDegree  = pitchRowStep % len(scale)         # find index into scale list
   register     = pitchRowStep // len(scale)        # find octave/pitch register

   # rebuild pitch: octave + scale offset, then shift into the key
   mappedPitch = register * 12 + scale[scaleDegree] + key

   # now, mappedPitch has been sieved through the pitchSet and adjusted to fit

   mappedPitch = int(mappedPitch)   # force an int data type

   return mappedPitch


def mapList(valueList, minValue, maxValue, minResult, maxResult):
   """Convert a list of numbers from one range to their matching places relative to another range.

   Like map(), but for a whole list, so numbers may lie outside the source range. A new
   list is returned; the original list is left unchanged.

   Args:
       valueList (list[int or float]): The numbers to convert.
       minValue (int or float): The low end of the source range (inclusive).
       maxValue (int or float): The high end of the source range (inclusive).
       minResult (int or float): The low end of the destination range (inclusive).
       maxResult (int or float): The high end of the destination range (inclusive).

   Returns:
       mappedList (list[int or float]): Each number's matching place in the destination range.
   """
   mappedList = []

   for value in valueList:
      newValue = map(value, minValue, maxValue, minResult, maxResult)
      mappedList.append(newValue)

   return mappedList


def mapValueList(valueList, minValue, maxValue, minResult, maxResult):
   """Convert a list of numbers from one range to their matching places in another range.

   Like mapValue(), but for a whole list, so each number must lie within the source
   range. A new list is returned; the original list is left unchanged.

   Args:
       valueList (list[int or float]): The numbers to convert.
       minValue (int or float): The low end of the source range (inclusive).
       maxValue (int or float): The high end of the source range (inclusive).
       minResult (int or float): The low end of the destination range (inclusive).
       maxResult (int or float): The high end of the destination range (inclusive).

   Returns:
       mappedList (list[int or float]): Each number's matching place in the destination range.
   """
   mappedList = []

   for value in valueList:
      newValue = mapValue(value, minValue, maxValue, minResult, maxResult)
      mappedList.append(newValue)

   return mappedList


def mapScaleList(valueList, minValue, maxValue, minResult, maxResult, scale=None, key=None):
   """Convert a list of numbers from one range to their matching places in another range.

   Like mapScale(), but for a whole list.  A new list is returned; the original list is left unchanged.

   Args:
       valueList (list[int or float]): The numbers to convert.
       minValue (int or float): The low end of the source range (inclusive).
       maxValue (int or float): The high end of the source range (inclusive).
       minResult (int or float): The low end of the destination range (inclusive).
       maxResult (int or float): The high end of the destination range (inclusive).
       scale (list[int], optional): The scale to snap to, a list of pitch classes between 0 and 11. If omitted, every pitch is allowed (the chromatic scale).
       key (int, optional): The scale's root pitch class, from 0 to 11. If omitted, it is taken from minResult.

   Returns:
       mappedList (list[int or float]): Each number's matching place in the destination range.
   """
   mappedList = []

   for value in valueList:
      newValue = mapScale(value, minValue, maxValue, minResult, maxResult, scale, key)
      mappedList.append(newValue)

   return mappedList

#######################################################################################
# Float Range
#######################################################################################
# Python's normal range() only allows integer steps.  frange() allows for fractional steps.

def frange(start, stop, step):
   """Build a list of evenly spaced numbers, allowing fractional steps.

   Like Python's range(), but step may be a fraction, for example 0.5. The numbers are
   rounded to the number of decimal places in step. As with range(), stop is not
   included, and step may be negative to count down.

   Args:
       start (int or float): The first number.
       stop (int or float): The number to stop before (not included).
       step (int or float): The gap between numbers; may be negative to count down. Must not be zero.

   Returns:
       floatList (list[float]): The evenly spaced numbers from start up to (but not including) stop.
   """
   if step == 0:   # make sure we do not get into an infinite loop
      raise ValueError("frange() step argument must not be zero")

   floatList = []                         # holds resultant list
   # since Python's represetation of real numbers may not be exactly what we expect,
   # let's round to the number of decimals provided in 'step'
   accuracy = len(str(step-int(step))[1:])-1  # determine number of decimals in 'step'

   # determine which termination condition to use
   if step > 0:
      done = start >= stop
   else:
      done = start <= stop

   # generate sequence
   while not done:
      start = round(start, accuracy)  # use same number of decimals as 'step'
      floatList.append(start)
      start += step
      # again, determine which termination condition to use
      if step > 0:
         done = start >= stop
      else:
         done = start <= stop

   return floatList


def xfrange(start, stop, step):
   """Step through evenly spaced numbers one at a time, allowing fractional steps.

   A generator version of frange(): instead of building the whole list at once, it
   produces each number as you loop over it. This is handy for long ranges. As with range(),
   stop is not included, and step may be negative to count down.

   Args:
       start (int or float): The first number.
       stop (int or float): The number to stop before (not included).
       step (int or float): The gap between numbers; may be negative to count down. Must not be zero.

   Returns:
       value (float): The next number in the sequence, each time through the loop.
   """
   if step == 0:   # make sure we do not get into an infinite loop
      raise ValueError("frange() step argument must not be zero")

   # since Python's represetation of real numbers may not be exactly what we expect,
   # let's round to the number of decimals provided in 'step'
   accuracy = len(str(step-int(step))[1:])-1  # determine number of decimals in 'step'

   # determine which termination condition to use
   if step > 0:
      done = start >= stop
   else:
      done = start <= stop

   # generate sequence
   while not done:
      start = round(start, accuracy)  # use same number of decimals as 'step'
      yield start
      start += step
      # again, determine which termination condition to use
      if step > 0:
         done = start >= stop
      else:
         done = start <= stop

#######################################################################################
# Tests
#######################################################################################

if __name__ == "__main__":
   pass
