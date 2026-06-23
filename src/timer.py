###############################################################################
# timer.py       Version 2.0     22-Jun-2026
#
# Taj Ballinger, Trevor Ritchie, Drew Smuniewski, and Bill Manaris
#
###############################################################################
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
#
###############################################################################
#
# REVISIONS:
#
# 2.0   22-Jun-2026 (tb)   Ported from JythonMusic to PythonMusic.
#      - Replaced Java timers with single shared, drift-compensated Python ticker thread
#      - Guarded callbacks so one raised exception cannot kill ticker thread
#      - Merged former animate.py as Automate
#      - Added LinearRamp for smooth value ramps
#      - Replaced JEM Stop-button cleanup (registerStopFunction) with atexit shutdown
#      - Added full Google-style docstrings throughout
#
###############################################################################
#
# Timer class for scheduling tasks to run or repeat at fixed time intervals.
#

from utilities import *    # mapValue, etc.
import threading, time, atexit
import numpy as np

############### Timer ########################################################
# To work around the limitation that we can't easily schedule callbacks
# at specific times, we create a ticker thread that wakes up at
# short intervals to check if any timers need to be triggered.
#
# ACCURACY ADVANTAGES:
# 1. Running in a separate thread means timing isn't affected by operations
#    in the main thread.
# 2. Measuring actual elapsed time (dt) compensates for any processing delays
# 3. Accumulating precise time values prevents long-term drift
#
# LIMITATIONS:
# - There is ONE shared ticker thread for the whole module, no matter how many Timer
#   instances exist or how many callbacks are registered. All callbacks run on that
#   single thread, one after another, so a slow callback delays every other timer
#   (and the tick loop itself).
# - The ticker wakes about every 10 ms, and each timer fires at most once per wake, so
#   intervals shorter than ~10 ms cannot be honored accurately (they drift and may drop
#   events). 60 fps (~16.6 ms) and slower is safely within range.
#
# Timers are added to _activeTimers when they start, and removed when they stop
# or, if they are oneshots, when they call their callback function.
###############################################################################

class Timer:
   """Schedule a function to run after a delay, or to repeat at a fixed interval.

   A Timer waits the given interval, then calls your function, and either stops or keeps
   calling it at that interval. Start it with start(), and stop it with stop().

   The Timer keeps a reference to the parameters list, not a copy. Changing the list's
   contents (for example, parameters[0] = 3) affects later calls; replacing the variable
   with a brand-new list does not.

   Args:
       timeInterval (int or float): How long to wait before each call, in milliseconds.
       action (Callable): The function to call; it should accept as many parameters as the parameters list holds.
       parameters (list, optional): The parameters to pass to the function each time it is called. Defaults to none.
       repeat (bool, optional): Whether to keep calling the function at the interval (True) or call it just once (False).
   """

   def __init__(self, timeInterval, action, parameters=None, repeat=True):
      self._interval   = timeInterval / 1000.0  # convert ms to seconds
      self._action     = action                 # callback function to execute
      self._parameters = parameters if parameters is not None else []   # avoid a shared mutable default
      self._repeat     = repeat                 # whether to repeat the timer or run once
      self._scheduled  = False                  # flag indicating if timer is scheduled
      self._accumulatedTime = 0                 # tracks elapsed time since last execution
      self._running = False                     # flag indicating if timer is currently running

   def __str__(self):
      return f"Timer(timeInterval = {self.getDelay()}, action = {self._action}, parameters = {self._parameters}, repeat = {self.getRepeat()})"

   def __repr__(self):
      return str(self)

   def _tick(self, dt):
      """"""
      if not self._running:
         return

      # accumulate the actual elapsed time with high precision
      self._accumulatedTime += dt

      # check if it's time to run the callback
      if self._accumulatedTime >= self._interval:
         # call the action function; guard it so a raised callback can never
         # crash the single ticker thread that drives every timer in the program
         try:
            self._action(*self._parameters)
         except Exception as error:
            print(f"Timer(): action '{self._action.__name__}' raised {error}.")

         # reset accumulated time, accounting for overshooting
         if self._repeat:
            # DRIFT PREVENTION: subtract exactly one interval, preserving any excess time
            # this is critical for preventing long-term drift in repeated timers
            self._accumulatedTime -= self._interval
         else:
            # for one-shot timers, remove from active timers
            self.stop()

   def start(self):
      """Start the timer.

      It begins counting, and calls your function once the interval has passed.
      """
      # check if timer is not already running
      if not self._running:
         self._running = True         # set running flag to true
         self._accumulatedTime = 0    # reset accumulated time
         _activeTimers.append(self)   # add this timer to the active timers list

   def stop(self):
      """Stop the timer.

      Your function stops being called until the timer is started again.
      """
      # check if timer is currently running
      if self._running:
         self._running = False         # set running flag to false

         # remove this timer from the active timers list
         # (use try/except rather than a membership check: another thread may remove it
         #  between the check and the remove, which would raise ValueError)
         try:
            _activeTimers.remove(self)
         except ValueError:
            pass   # already removed by another thread

   def getDelay(self):
      """Return the timer's interval.

      Returns:
          timeInterval (int or float): The wait between calls, in milliseconds.
      """
      timeInterval = self._interval * 1000   # convert back to ms for API consistency
      return timeInterval

   def setDelay(self, timeInterval):
      """Set the timer's interval.

      If the timer is running, the new interval takes effect right away.

      Args:
          timeInterval (int or float): The new wait between calls, in milliseconds.
      """
      self._interval = timeInterval / 1000.0

      # if running, restart with new interval
      if self.isRunning():
         self.stop()
         self.start()

   def isRunning(self):
      """Report whether the timer is running.

      Returns:
          isRunning (bool): True if the timer has been started and not stopped, False otherwise.
      """
      isRunning = self._running
      return isRunning

   def setFunction(self, action, parameters=None):
      """Set the function the timer calls.

      Args:
          action (Callable): The function to call; it should accept as many parameters as the parameters list holds.
          parameters (list, optional): The parameters to pass to the function each time it is called. Defaults to none.
      """
      self._action = action
      self._parameters = parameters if parameters is not None else []   # avoid a shared mutable default

   def getRepeat(self):
      """Report whether the timer repeats.

      Returns:
          isRepeating (bool): True if the timer repeats, False if it runs once.
      """
      isRepeating = self._repeat
      return isRepeating

   def setRepeat(self, repeat):
      """Set whether the timer repeats.

      Args:
          repeat (bool): True to keep calling the function at the interval, False to call it just once.
      """
      self._repeat = repeat


# global ticker thread that calls timer callbacks
def _tickerThread():
   """"""

   lastTime = time.perf_counter()   # monotonic clock: immune to wall-clock / NTP jumps
   while _tickerRunning:
      currentTime = time.perf_counter()
      dt = currentTime - lastTime  # measure actual elapsed time between ticks
      lastTime = currentTime

      # call tick for all active timers with the precise time difference;
      # guard each one so a single misbehaving timer can never kill this thread
      for timer in list(_activeTimers):
         try:
            timer._tick(dt)
         except Exception as error:
            print(f"Timer: tick error {error}.")

      # sleep for a short time (adjust as needed for precision)
      time.sleep(0.01)  # 10ms resolution - balances CPU usage with timing precision


# register cleanup on exit
def _cleanup():
   """"""
   global _tickerRunning
   _tickerRunning = False

   # stop all active timers
   for timer in list(_activeTimers):
      timer.stop()


# Module-level engine setup. This runs once, when the module is first imported
# (Python caches imports, so it never runs a second time).
_activeTimers = []
_tickerRunning = True

# allow Python to exit even if thread is running
_ticker = threading.Thread(target=_tickerThread, daemon=True)
_ticker.start()

# NOTE: We don't need a blocking thread when using python -i,
# since the interpreter stays open already

atexit.register(_cleanup)   # cleanup active timers at exit


#######################################################################################
# Automate
#######################################################################################
# The Automate class provides a simplified way to automate repeated calling of functions
# for automation or other automation effects. Examples may range from continuously animating 
# GUI graphics (similar to MIT Processing's draw() loop), to sequencing precise, data-driven 
# musical automation (such as volume envelopes or filter sweeps). 
#
# It uses a single "master" timer, which makes sure that all visual, audio, and other effects
# are perfectly synchronized (unlike creating individual timers for each). This is very important.
#
# It provides an Automate static class that can register functions to call repeatedly to support various scenarios. 
# Anything more involved can be created using regular timers.
#
# Additionally, it provides a few shorthand functions, like automate(), setAutomationRate(), etc.
#
# NOTE:  Automation engine is initialized (i.e., master timer starts ticking) after the first callback
#        is added, not when the module is loaded.

class Automate:
   """Call functions repeatedly, all kept in step by one shared clock.

   Automate is a static utility. Call its methods on the class itself, for example
   Automate.add(). It drives repeated calls (animating graphics, sweeping a volume or
   filter, stepping through data, and so on) from a single master timer, so every effect
   stays perfectly in sync. The timer starts as soon as the library is loaded, and its
   rate is measured in frames per second.
   """
   _ENGINE     = None             # master timer, created and started at module load time
   _interval   = 1000.0 / 60.0    # current timer interval (in ms)
   _actionList = []               # list of registered callback functions to automate


   @staticmethod
   def _init():
      """"""

      # initialize only if engine has not been created previously
      if Automate._ENGINE is None:   # no engine available? 

         # yes, so create a new engine and start it
         from timer import Timer

         # use a regular timer (i.e., our master timer) to call every interval
         # our tick function (which in turns calls all registered functions appropriately)
         # Timer(delay, callback, arguments, repeat)
         Automate._ENGINE = Timer(Automate._interval, Automate._tick, [], True)   # create it
         Automate._ENGINE.start()                                               # and start it!!!

      # now, the master timer is running, ready to call any function that gets registered


   @staticmethod
   def _tick():
      """"""
      # iterate through the list of registered actions
      for action in Automate._actionList:

         if callable(action):   # is this a function?

            # yes, so execute it!!
            action()

      # now, all registered functions have been called one time


   @staticmethod
   def resume():
      """Resume automation after a pause.

      Picks up where pause() left off, calling every registered function again.
      """

      if Automate._ENGINE is not None:   # do we have an engine?

         # yes, so resume it (starting it continues where we left off...)
         Automate._ENGINE.start()


   @staticmethod
   def pause():
      """Pause automation.

      Every registered function stops being called until resume(); nothing is lost in the
      meantime.
      """

      if Automate._ENGINE is not None:   # do we have an engine?

         # yes, so pause it (stopping simply stops ticking - everything else remains in place!!)
         Automate._ENGINE.stop()


   @staticmethod
   def add(action):
      """Register a function to be called once every frame.

      Use setRate() to change how often that is.

      Args:
          action (Callable): The function to call; it receives no parameters.
      """

      if callable(action):   # is this a function?
         # yes, so add it to list of functions to be called
         Automate._actionList.append(action)

         # and ensure that the automate engine is started
         Automate._init()

      else:

         # let them know that something is wrong...
         print(f"Automate.add(): '{action}' is not a callable function.")


   @staticmethod
   def addWithValues(action, values, duration=None, repeat=1, whenDone=None):
      """Step a function through a list of values, evenly spaced over time.

      Calls the function once for each value in turn, handing it the current value. Good for
      sweeping a setting smoothly through a series of numbers.

      Args:
          action (Callable): The function to call; it receives one parameter, the current value.
          values (list): The values to step through, in order.
          duration (int or float, optional): How long the whole list takes, in seconds. If omitted, one value is delivered per frame.
          repeat (int, optional): How many times to run through the list; use -1 to repeat forever.
          whenDone (Callable, optional): A function to call once, after the last run through the list; it receives no parameters.
      """

      if not callable(action):   # is it NOT a function?

         # let them know something is wrong...
         print(f"Automate.addWithValues(): '{action}' is not a callable function.")

      elif len(values) == 0:     # is the list empty?

         # let them know something is wrong...
         print("Automate.addWithValues(): 'values' list is empty.")

      else:   # value list is not empty, so...

         if duration is None:   # default duration?

            timeDelayBetweenValues = Automate._interval   # use engine's default interval

         else:   # they have provided their own time-stretching, so...

            # calculate time delay (in millisecs) between values
            timeDelayBetweenValues = (duration * 1000.0) / len(values)

         # now, timeDelayBetweenValues contains how long we should wait to process next value... 

         # check if this makes sense...
         if timeDelayBetweenValues < Automate._interval:   # is duration provided too small for our frame rate?
            
            # calculate the minimum possible duration for the error message
            minAllowableDuration = (Automate._interval * len(values)) / 1000.0
            
            # let them know something is wrong...
            print(f"Automate.addWithValues(): duration ({duration}s) is too short to process, given frame rate ({Automate.getRate()})")
            print(f"                         Should be at least {minAllowableDuration:.2f} secs.")

         else:   # all good, so proceed...

            import time

            #####
            # Now, we will build a closure (inner function) to handle processing each individual value, 
            # as well as anything else that may need to happen (i.e., start over for the next repetition,
            # or call the 'whenDone' function if we are completely done - after the last value).

            # A closure needs some non-local (i.e., external to it) variables to remember how far it has gone.

            # NOTE:  Every time addWithValues() above gets called, new variables are created here, 
            #        and these are combined with the closure below, maintaining its state persistently
            #        without overwriting each other - it works well.

            # external variables to be wrapped within the closure
            valuesIndex   = 0   # points to next value to be processed
            repeatCounter = 0   # how many repetitions done so far

            # timer delay (in millisecs) for each value
            delay = timeDelayBetweenValues
            
            # remembers when the previous execution happened
            previousTime = time.time() * 1000.0   # initialize to "now"...

            # define an inner function (closure) that contains the logic of what to do 
            # with each provided value... 
            def processEachValueClosure():
               nonlocal previousTime    # remembers when previous execution happened
               nonlocal valuesIndex     # remembers which value is to be processed this time
               nonlocal repeatCounter   # remembers how many times we have processed the complete value list

               # get current time (in millisecs)
               currentTime = time.time() * 1000.0
               
               # has enough time passed to trigger the next value?
               if (currentTime - previousTime) >= delay:
                  
                  # yes, update time tracker
                  previousTime = previousTime + delay
                  
                  # act only if there are remaining values to be processed
                  if valuesIndex < len(values):   # any left?
                     
                     # yes, so...
                     
                     # get next value
                     value = values[valuesIndex]
                     
                     # NOTE: this is the important step that advances the automation!!!
                     action(value)   # execute the original callback with the current value 
                     
                     # point to next value to be processed (if any)
                     valuesIndex = valuesIndex + 1

                  # now, the current value has been processed...
                     
                  # have we completed processing all the values?
                  if valuesIndex >= len(values):   # no more values left?
                     
                     # yes, we are done... so, advance to the next repetition (if any)
                     repeatCounter = repeatCounter + 1

                     # do we have more repetitions?
                     if repeat == -1 or repeatCounter < repeat:   
                        
                        # yes, so start processing values once more
                        valuesIndex = 0   # point to first value

                     else:   # we are done repeating, so...

                        # remove this inner function from the engine...
                        Automate.remove( processEachValueClosure )
                        
                        # and execute the callback (if any)
                        if callable(whenDone):   # is there a completion callback?
                           
                           # yes, so execute it!!
                           whenDone()

               # now, we have finished processing current value, and have taken care
               # of anything else that may have needed to happen (i.e., start over next repetition,
               # or called 'whenDone' function, if we are completely done - after this value) 

            # NOTE:  Very important - now that this inner function has been built, 
            #        we need to register it with our engine, so it can do its job...

            # register the closure to be called - it will take care of everything else...
            Automate._actionList.append(processEachValueClosure)


   @staticmethod
   def addWithTimedValues(action, values, times, duration=None, repeat=1, whenDone=None):
      """Step a function through a list of values, each delivered at its own time.

      Like addWithValues(), but you give the exact moment for each value instead of spacing
      them evenly. The values and times lists are parallel, and the times must increase.

      Args:
          action (Callable): The function to call; it receives one parameter, the current value.
          values (list): The values to step through, in order.
          times (list[int or float]): When to deliver each value, in seconds from the start of the sequence; each must be later than the one before.
          duration (int or float, optional): Stretch or squeeze the whole sequence to last this many seconds. If omitted, the times are used as given.
          repeat (int, optional): How many times to run through the sequence; use -1 to repeat forever.
          whenDone (Callable, optional): A function to call once, after the last run through the sequence; it receives no parameters.
      """

      if not callable(action):   # is it NOT a function?

         # let them know that something is wrong...
         print(f"Automate.addWithTimedValues(): '{action}' is not a callable function.")

      elif len(values) == 0:     # is the list empty?

         # let them know that something is wrong...
         print("Automate.addWithTimedValues(): 'values' list is empty.")

      elif len(values) != len(times):   # are the lists not parallel?

         # let them know that something is wrong...
         print(f"Automate.addWithTimedValues(): length of 'values' ({len(values)}) and 'times' ({len(times)}) must be the same.")

      else:   # lists are non-empty and parallel, so...

         # calculate all raw intervals between consecutive times
         # (if list has only 1 item, intervals will be empty)
         intervals = [times[i] - times[i-1] for i in range(1, len(times))]

         # check for simultaneous or out-of-order timestamps
         if len(intervals) > 0 and min(intervals) <= 0:

            # let them know that something is wrong...
            print(f"Automate.addWithTimedValues(): all timestamps should be larger than their previous one.")

         else:   # timestamps are valid and strictly increasing, so check engine limits...

            # initialize default time scale (no time-stretching)
            timeScale = 1.0

            if duration is not None:   # did they provide duration?

               # find the original duration (very last element in the times sequence)
               originalDuration = float(times[-1])

               if originalDuration > 0:

                  # calculate scale factor to stretch/compress the overall timing
                  timeScale = (duration * 1000.0) / originalDuration

            # adjust the smallest raw interval by our timeScale to see what the engine will actually process
            isTooSmall = False
            
            if len(intervals) > 0:
               
               minInterval = min(intervals) * timeScale
               
               if minInterval < Automate._interval:   # is the smallest gap too tight?
                  
                  isTooSmall = True   # remember that

            # now, either isTooSmall is True, meaning the tightest gap is invalid, or
            # it is False, meaning all intervals are valid 

            if isTooSmall:   # did we find an interval that is too small?
               
               # calculate what the scale factor WOULD need to be to make the smallest gap fit the engine
               # (we can safely divide by min(intervals) here because we proved > 0 in the previous block)
               requiredScaleFactor = Automate._interval / float(min(intervals))
               
               # calculate the minimum allowable duration (in seconds) based on that scale factor
               originalDuration = float(times[-1])
               minAllowableDuration = (requiredScaleFactor * originalDuration) / 1000.0
               
               if duration is not None:   # did they provide a duration?
                  
                  # let them know their duration is too short
                  print(f"Automate.addWithTimedValues(): duration ({duration} secs) is too small to process, given frame rate ({Automate.getRate()}).")
                  print(f"                              Should be at least {minAllowableDuration:.2f} secs.")
                  
               else:   # they didn't provide a duration, but the raw timestamps are too tight
                  
                  # let them know they need to stretch the sequence
                  print(f"Automate.addWithTimedValues(): found time interval that is too small ({minInterval} secs), given frame rate ({Automate.getRate()}).")
                  print(f"                              Increase interval between times, or provide a duration of at least {minAllowableDuration:.2f} secs.")
            
            else:   # all good, so proceed...

               import time

               #####
               # Now, we will build a closure (inner function) to handle processing each individual value, 
               # as well as anything else that may need to happen (i.e., start over for the next repetition,
               # or call the 'whenDone' function if we are completely done - after the last value).

               # A closure needs some non-local (i.e., external to it) variables to remember how far it has gone.

               # NOTE:  Every time addWithTimedValues() above gets called, new variables are created here, 
               #        and these are combined with the closure below, maintaining its state persistently
               #        without overwriting each other - it works well.

               # external variables to be wrapped within the closure
               valuesIndex   = 0   # points to next value to be processed
               repeatCounter = 0   # how many repetitions done so far

               # remembers when the current automation sequence started
               sequenceStartTime = time.time() * 1000.0   # initialize to "now"...

               # define an inner function (closure) that contains the logic of what to do 
               # with each provided value... 
               def processEachTimedValueClosure():
                  nonlocal sequenceStartTime   # remembers when the current sequence repetition started
                  nonlocal valuesIndex         # remembers which value is to be processed this time
                  nonlocal repeatCounter       # remembers how many times we have processed the complete value list

                  # get current time (in millisecs)
                  currentTime = time.time() * 1000.0
                  
                  # calculate how much time has elapsed since the sequence started
                  elapsedTime = currentTime - sequenceStartTime
                  
                  # get the target timestamp directly from the times list (adjusted by our timeScale)
                  targetTimestamp = times[valuesIndex] * timeScale

                  # has enough time passed to trigger the next value based on its target timestamp?
                  if elapsedTime >= targetTimestamp:
                     
                     # yes, so...
                     
                     # get the arguments directly from the values list
                     actionArgs = values[valuesIndex]
                     
                     # NOTE: this is the important step that advances the automation!!!
                     # unpack the arguments (*) and execute the original callback
                     action(*actionArgs)   
                     
                     # point to next value to be processed (if any)
                     valuesIndex = valuesIndex + 1

                     # now, the current value has been processed...
                        
                     # have we completed processing all the values?
                     if valuesIndex >= len(values):   # no more values left?
                        
                        # yes, we are done... so, advance to the next repetition (if any)
                        repeatCounter = repeatCounter + 1

                        # do we have more repetitions?
                        if repeat == -1 or repeatCounter < repeat:   
                           
                           # yes, so start processing values once more
                           valuesIndex = 0   # point to first value
                           
                           # reset the sequence start time for the next repetition cycle
                           sequenceStartTime = time.time() * 1000.0

                        else:   # we are done repeating, so...

                           # remove this inner function from the engine...
                           Automate.remove( processEachTimedValueClosure )
                           
                           # and execute the callback (if any)
                           if callable(whenDone):   # is there a completion callback?
                              
                              # yes, so execute it!!
                              whenDone()

                  # now, we have finished processing current value, and have taken care
                  # of anything else that may have needed to happen (i.e., start over next repetition,
                  # or called 'whenDone' function, if we are completely done - after this value) 

               # NOTE:  Very important - now that this inner function has been built, 
               #        we need to register it with our engine, so it can do its job...

               # register the closure to be called - it will take care of everything else...
               Automate._actionList.append(processEachTimedValueClosure)


   @staticmethod
   def remove(action):
      """Stop calling a registered function.

      Args:
          action (Callable): The function to remove from automation.
      """
      
      if action in Automate._actionList:   # is this a previously registered function?

         # yes, so remove first matching occurrence
         Automate._actionList.remove(action)

      else:

         # let them know that something is wrong...
         print(f"Automate.remove(): '{action}' does not appear in the list of registered functions.")


   @staticmethod
   def getRate():
      """Return how often automation runs.

      Returns:
          frameRate (int): The current rate, in frames per second.
      """

      # convert milliseconds back to frames per second
      frameRate = int(1000.0 / Automate._interval)
      return frameRate


   @staticmethod
   def setRate(frameRate=60):
      """Set how often automation runs.

      Args:
          frameRate (int, optional): The new rate, in frames per second.
      """

      # convert frames per second to milliseconds
      Automate._interval = (1000.0 / frameRate)
      
      if Automate._ENGINE is not None:   # do we have an engine?

         # yes, so update the engine
         Automate._ENGINE.setDelay(Automate._interval)


####
# function aliases for backwards compatibility / simplicity
def automate(action):
   """Register a function to be called repeatedly, once every frame.

   Shorthand for Automate.add().

   Args:
       action (Callable): The function to call; it receives no parameters.
   """
   Automate.add(action)


def setAutomationRate(frameRate=60):
   """Set how often automation runs.

   Shorthand for Automate.setRate().

   Args:
       frameRate (int, optional): The new rate, in frames per second.
   """
   Automate.setRate(frameRate)


def getAutomationRate():
   """Return how often automation runs.

   Shorthand for Automate.getRate().

   Returns:
       frameRate (int): The current rate, in frames per second.
   """
   frameRate = Automate.getRate()
   return frameRate


def pauseAutomation():
   """Pause automation.

   Shorthand for Automate.pause().
   """
   Automate.pause()


def resumeAutomation():
   """Resume automation after a pause.

   Shorthand for Automate.resume().
   """
   Automate.resume()


#######################################################################################
# LinearRamp
#######################################################################################
# Creates a linear ramp that calls a function at regular intervals with interpolated values.
# - delay: total duration of the ramp in milliseconds
# - startValue: value at the start of the ramp
# - endValue: value at the end of the ramp
# - function: callback function to call with the current interpolated value
# - step: interval between function calls in milliseconds (default: 10)
#
# The ramp will smoothly transition from startValue to endValue over delay milliseconds,
# calling the provided function at regular intervals with the current interpolated value.
# The function should accept a single argument representing the current ramp value.
#######################################################################################

class LinearRamp:
   """Slide a value smoothly from one number to another over time, calling a function as it changes.

   A LinearRamp moves a value from a start to an end over a set time, calling your
   function with the current value at each small step along the way. This is handy for fading
   volume, moving graphics, and other gradual changes. Start it with start(), and aim it
   somewhere new with setTarget() while it runs.

   Args:
       delay (int or float): How long the whole ramp takes, in milliseconds.
       startValue (int or float): The value to start from.
       endValue (int or float): The value to end at.
       action (Callable): The function to call as the value changes; it receives one parameter, the current value.
       step (int, optional): How often to update the value and call the function, in milliseconds.
   """

   def __init__(self, delay, startValue, endValue, action, step=10):
      # remember callback function and step interval
      self._action = action
      self._step = self._sanitizeStep(step)
      self._timer  = None

      # initialize value tracking
      self._currentValue = startValue
      self._sourceValue = startValue
      self._targetValue = endValue

      # initialize timing variables
      self._delay = 0.0
      self._durationSeconds = 0.0
      self._ratePerSecond = 0.0

      # initialize ramp state
      self._phase = 0.0
      self._isRunning = False
      self._lastTickTime = None

      # set the ramp duration
      self._setDuration(delay)

      # make sure action is callable
      if not callable(action):
         print("LinearRamp: Error - action must be callable.")

   def __str__(self):
      return (f"LinearRamp(delay={self._delay}, currentValue={self._currentValue}, "
              f"targetValue={self._targetValue}, step={self._step})")

   def __repr__(self):
      return str(self)

   def start(self):
      """Start the ramp from its current value toward its target.

      Calls your function right away with the starting value, then again at each step until
      it reaches the target. If the ramp was already running, it restarts from where it is.
      """
      # make sure action is callable
      if not callable(self._action):
         print("LinearRamp: Error - callback action must be callable to start.")
         return

      # stop if already running
      if self._isRunning:
         self.stop()

      # initialize ramp from current value
      self._sourceValue = self._currentValue
      self._phase = 0.0
      self._lastTickTime = time.perf_counter()

      # notify with initial value
      self._notify()

      # handle immediate execution for zero or negative delay
      if self._delay <= 0:
         self._completeImmediately()
         return

      # create and start the timer
      self._ensureTimer()
      self._isRunning = True
      self._timer.start()

   def stop(self):
      """Stop the ramp where it is.

      Your function stops being called until the ramp is started again.
      """
      if self._timer:   # stop the timer if it exists
         self._timer.stop()
      self._isRunning = False   # clear running flag
      self._lastTickTime = None   # reset tick time

   def setTarget(self, targetValue, delay=None):
      """Aim the ramp at a new value, starting from where it is now.

      You can also change how long the ramp takes. If the ramp was not running, this starts
      it.

      Args:
          targetValue (int or float): The new value to ramp toward.
          delay (int or float, optional): A new length for the ramp, in milliseconds. If omitted, the current length is kept.
      """
      # update target value
      self._targetValue = targetValue

      # update duration if provided
      if delay is not None:
         self._setDuration(delay)

      # reset ramp to start from current value
      self._sourceValue = self._currentValue
      self._phase = 0.0
      self._lastTickTime = time.perf_counter()

      # notify with current value
      self._notify()

      # handle immediate execution for zero or negative delay
      if self._delay <= 0:
         self._completeImmediately()
         return

      # start the timer if not already running
      if not self._isRunning:
         self._ensureTimer()
         self._isRunning = True
         self._timer.start()

   def setDuration(self, delay):
      """Change how long the ramp takes.

      Args:
          delay (int or float): The new length for the ramp, in milliseconds.
      """
      # update duration
      self._setDuration(delay)

      # handle immediate execution for zero or negative delay
      if self._delay <= 0:
         self._completeImmediately()
         return

      # reset tick time if running
      if self._isRunning:
         self._lastTickTime = time.perf_counter()

   def isRunning(self):
      """Report whether the ramp is running.

      Returns:
          isRunning (bool): True if the ramp is still moving, False otherwise.
      """
      isRunning = self._isRunning
      return isRunning

   def getCurrentValue(self):
      """Return the ramp's current value.

      Returns:
          value (int or float): The value right now, somewhere between the start and the target.
      """
      value = self._currentValue
      return value

   def _ensureTimer(self):
      """"""
      if self._timer is None:   # create new timer
         self._timer = Timer(timeInterval=self._step,
                              action=self._tick,
                              parameters=[],
                              repeat=True)
      else:   # reconfigure existing timer
         self._timer.setDelay(self._step)
         self._timer.setFunction(self._tick, [])
         self._timer.setRepeat(True)

   def _tick(self):
      """"""
      if not self._isRunning:   # exit if not running
         return

      # measure elapsed time since last tick
      now = time.perf_counter()
      if self._lastTickTime is None:   # first tick, just initialize
         self._lastTickTime = now
         return

      dt = now - self._lastTickTime   # calculate time delta
      self._lastTickTime = now

      # update phase based on elapsed time
      if self._durationSeconds <= 0:
         self._phase = 1.0   # instant completion
      else:
         self._phase += dt * self._ratePerSecond   # advance phase proportionally

      # check if ramp is complete
      if self._phase >= 1.0:
         self._phase = 1.0   # clamp to 1.0
         self._currentValue = self._targetValue   # ensure exact target value
         self._notify()   # notify with final value
         self.stop()   # stop the ramp
      else:   # ramp in progress
         # calculate interpolated value
         self._currentValue = self._sourceValue + (self._phase * (self._targetValue - self._sourceValue))
         self._notify()   # notify with current value

   def _completeImmediately(self):
      """"""
      self._phase = 1.0   # set phase to complete
      self._currentValue = self._targetValue   # jump to target value
      self._notify()   # notify with final value
      self.stop()   # stop the ramp

   def _notify(self):
      """"""
      if not callable(self._action):   # skip if action is not callable
         return

      # call the callback function with error handling
      try:
         self._action(self._currentValue)
      except Exception as error:
         print(f"LinearRamp: Warning - callback raised {error}.")

   def _setDuration(self, delay):
      """"""
      # validate and convert delay to float
      try:
         delay = float(delay)
      except (TypeError, ValueError):
         delay = 0.0

      # ensure non-negative delay
      if delay < 0:
         delay = 0.0

      # store duration in milliseconds and seconds
      self._delay = delay
      self._durationSeconds = delay / 1000.0

      # calculate rate per second for phase advancement
      if self._durationSeconds <= 0:
         self._ratePerSecond = 0.0   # instant completion
      else:
         self._ratePerSecond = 1.0 / self._durationSeconds   # phase units per second

   def _sanitizeStep(self, step):
      """"""
      # validate and convert step to float
      try:
         step = float(step)
      except (TypeError, ValueError):
         step = 10.0   # default to 10ms if invalid

      # ensure positive step value
      if step <= 0:
         step = 10.0   # default to 10ms if non-positive

      return step


# tests
if __name__ == '__main__':
   seconds = 0
   startTime = time.time()

   def echoTime():
      global seconds
      current = seconds
      seconds += 1
      print(f"Timed Seconds: {current+1}, Actual Seconds: {time.time()-startTime:.3f}")

   # define timer to count and output elapsed time (in seconds)
   t = Timer(1000, echoTime, [], True)
   t.start()

   # test LinearRamp
   print("\n--- LinearRamp Test (0 to 10 over 2 seconds) ---")
   rampStartTime = time.time()
   def printRampValue(value):
      """"""
      print(f"Ramp Value: {value:.2f} at {time.time() - rampStartTime:.3f}s")

   # ramp from 0 to 10 over 2 seconds, with steps approx every 200ms
   ramp = LinearRamp(delay=2000, startValue=0, endValue=10, action=printRampValue, step=200)
   ramp.start()

#######################################################################################
# OscillatorTimer
#######################################################################################

class OscillatorTimer:
   """Call a function over and over with a value that oscillates between two bounds.

   An OscillatorTimer moves a value smoothly up and down between a minimum and a maximum,
   following a cosine wave, and calls your function with that value every delay
   milliseconds. It is handy for fluctuating a sound's volume, panning, or frequency,
   among other things. Start it with start(), and stop it with stop().

   Args:
       delay (int or float): How long to wait between updates, in milliseconds.
       minValue (int or float): The lowest value to oscillate down to.
       maxValue (int or float): The highest value to oscillate up to.
       step (int or float): How far the value moves each update, from 0 to (maxValue - minValue).
       action (Callable): The function to call each update; it receives one parameter, the current value.
   """

   def __init__(self, delay, minValue, maxValue, step, action):
      self._minValue = minValue   # the bottom of the oscillation
      self._maxValue = maxValue   # the top of the oscillation
      self._action   = action     # the function to call with each value

      # the value follows a cosine wave; the phase runs from 0 to 2*pi and wraps around
      self._phase = 0.0
      self._value = mapValue(np.cos(self._phase), -1.0, 1.0, self._minValue, self._maxValue)

      # turn the step (in value units) into how far the phase advances each update
      self._phaseStep = mapValue(step, 0.0, self._maxValue - self._minValue, 0.0, 2 * np.pi)

      # an internal timer drives the oscillation, calling _oscillate every 'delay' ms
      self._timer = Timer(delay, self._oscillate, [], True)

   def __str__(self):
      return (f"OscillatorTimer(delay = {self._timer.getDelay()}, "
              f"minValue = {self._minValue}, maxValue = {self._maxValue})")

   def __repr__(self):
      return str(self)

   def start(self):
      """Start the oscillator and begin calling your function.
      """
      self._timer.start()

   def stop(self):
      """Stop the oscillator.

      Your function stops being called until the oscillator is started again.
      """
      self._timer.stop()

   def setDelay(self, delay):
      """Set how long the oscillator waits between updates.

      Args:
          delay (int or float): The new wait between updates, in milliseconds.
      """
      self._timer.setDelay(delay)

   def getDelay(self):
      """Return how long the oscillator waits between updates.

      Returns:
          delay (int or float): The wait between updates, in milliseconds.
      """
      return self._timer.getDelay()

   def _oscillate(self):
      """"""
      # hand the current value to the function, then work out the next one
      self._action(self._value)
      self._phase = (self._phase + self._phaseStep) % (2 * np.pi)
      self._value = mapValue(np.cos(self._phase), -1.0, 1.0, self._minValue, self._maxValue)


#######################################################################################
# EnvelopeTimer
#######################################################################################

class EnvelopeTimer:
   """Call a function with a series of values, each delivered at its own time.

   An EnvelopeTimer steps your function through a list of values at a matching list of
   times, and can cycle back to the start after the last value. It is handy for shaping a
   sound's volume, panning, or frequency over time. The values and times lists run in
   parallel, and the times are absolute milliseconds from the start, in increasing order.
   A value that is itself a list or tuple is unpacked into several arguments to the
   function. Start it with start(), and stop it with stop().

   Args:
       action (Callable): The function to call; it receives the current value, or several arguments if the value is a list or tuple.
       values (list): The values to deliver, in order.
       times (list[int or float]): When to deliver each value, in milliseconds from the start; each must be later than the one before.
       repeat (bool, optional): Whether to cycle back to the start after the last value (True) or stop (False).
   """

   def __init__(self, action, values, times, repeat=False):
      self._action = action
      self._values = values
      self._times  = times
      self._repeat = repeat

      # the values and times lists run in parallel, so they must be the same length
      if len(self._values) != len(self._times):
         raise ValueError("EnvelopeTimer: 'values' and 'times' must be the same length "
                          f"(they were {len(self._values)} and {len(self._times)}).")

      self._pointCount = len(self._times)

      # the times must increase, so each value arrives after the one before it
      for i in range(self._pointCount - 1):
         if self._times[i] >= self._times[i + 1]:
            raise ValueError("EnvelopeTimer: 'times' must be increasing milliseconds "
                             f"(they were {self._times}).")

      # a value that is a list or tuple is unpacked into several arguments when called
      self._valuesAreGrouped = self._pointCount > 0 and isinstance(self._values[0], (list, tuple))

      self._index   = 0       # which value comes next
      self._paused  = False
      self._elapsed = 0.0     # envelope time already counted, in ms (frozen while paused)
      self._clock   = None    # clock reading when the current run began, or None when not running

      # an internal timer wakes often to check whether the next value's time has arrived
      self._timer = Timer(10, self._advance, [], True)   # check about every 10 ms

   def __str__(self):
      return (f"EnvelopeTimer(values = {self._values}, times = {self._times}, "
              f"repeat = {self._repeat})")

   def __repr__(self):
      return str(self)

   def start(self):
      """Start the envelope from the beginning.
      """
      self._elapsed = 0.0
      self._index   = 0
      self._paused  = False
      self._clock   = time.perf_counter()
      self._timer.start()

   def stop(self):
      """Stop the envelope and reset it to the beginning.
      """
      self._elapsed = 0.0
      self._index   = 0
      self._paused  = False
      self._clock   = None
      self._timer.stop()

   def pause(self):
      """Pause the envelope, remembering where it is.

      Use resume() to continue from this point.
      """
      # fold the time run so far into the running total, then freeze the clock
      if self._clock is not None:
         self._elapsed += (time.perf_counter() - self._clock) * 1000.0
         self._clock = None
      self._paused = True
      self._timer.stop()

   def resume(self):
      """Resume the envelope from where it was paused.
      """
      self._clock  = time.perf_counter()
      self._paused = False
      self._timer.start()

   def isRunning(self):
      """Report whether the envelope is running.

      Returns:
          isRunning (bool): True if the envelope is running, False otherwise.
      """
      return self._timer.isRunning()

   def isPaused(self):
      """Report whether the envelope is paused.

      Returns:
          isPaused (bool): True if the envelope is paused, False otherwise.
      """
      return self._paused

   def _advance(self):
      """"""
      # the envelope time is the running total plus however long the current run has gone
      if self._clock is None:
         return
      elapsed = self._elapsed + (time.perf_counter() - self._clock) * 1000.0

      # deliver every value whose time has now arrived
      while self._index < self._pointCount and elapsed >= self._times[self._index]:
         value = self._values[self._index]
         if self._valuesAreGrouped:   # a list or tuple becomes several arguments
            self._action(*value)
         else:
            self._action(value)
         self._index += 1

      # once every value has been delivered, either loop back or stop
      if self._index >= self._pointCount:
         if self._repeat:
            self._elapsed = 0.0
            self._index   = 0
            self._clock   = time.perf_counter()
         else:
            self.stop()

#######################################################################################
# Tests
#######################################################################################

if __name__ == "__main__":
   pass
