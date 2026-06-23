#######################################################################################
# iannix.py     Version 1.1     26-Aug-2025
#
# Taj Ballinger, Trevor Ritchie, Seth Stoudenmier, and Bill Manaris
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
#
#######################################################################################
#
# REVISIONS:
#
# 1.1   26-Aug-2025 (tr)   Ported from JythonMusic to PythonMusic.
#      - Fixed IannixOut default ipAddress to string "127.0.0.1", was unquoted and would not import
#      - Fixed addPointToCurve() Bezier control-point arguments, referenced undefined names
#      - Rewrote addPointListToCurve(), bad loop and indexing left it nonfunctional
#      - Added full Google-style docstrings throughout
#
#######################################################################################
#
# Inherits osc.py and works as the inbetween for PythonMusic and Iannix. Allows
# for messages to be received from and sent to Iannix through Open Sound Control.
#
#######################################################################################

from osc import OscIn, OscOut
from utilities import *    # mapValue, etc.


class IannixIn(OscIn):
   """Receive messages from a running IanniX application over OSC.

   IanniX is a graphic sequencer. As its score plays, IanniX sends out OSC messages for
   the triggers and cursors in the score, and for its transport controls (play, stop, and
   fast rewind). Create an IannixIn to listen on a port, then use the on... methods to run
   your own functions when those messages arrive. Extends OscIn.

   Args:
       port (int, optional): The port to listen on for messages from IanniX.
   """

   def __init__(self, port=57110):
      # initialize the OscIn port that is used by IannixIn
      OscIn.__init__(self, port)

      # dictionaries that will contain the functions that are passed value whenever
      # the corresponding OscIn address comes from Iannix
      self.transportActions = {"play":[], "stop":[], "fastrewind":[]}
      self.cursorActions = {}
      self.triggerActions = {}

      # NOTE: Functions that take in the osc messages are declared in the constructor because
      # they are only able to received one parameter, the message from the OscIn.onInput(),
      # however they need to be able to see the dictionaries that contain the functions
      # declared by the onTrigger, onCursor, and onTransport methods.

      def handleTransportMessage(message):
         args = message.getArguments()

         # values taken from the OscIn "/transport" address from Iannix
         state = args[0]
         timeStamp = float(args[1])

         # calling functions depending on which state is sent
         for action in self.transportActions[state]:
            action(timeStamp)

      def handleCursorMessage(message):
         args = message.getArguments()

         # values taken from OscIn "/cursor" address from Iannix
         cursorID = args[0]
         x = args[5]
         y = args[6]
         z = args[7]

         # calling functions depending on which cursor id is sent
         for action in self.cursorActions[cursorID]:
            action(x, y, z)

      def handleTriggerMessage(message):
         args = message.getArguments()

         # values taken from OscIn "/trigger" address from Iannix
         triggerID = args[0]
         x = args[5]
         y = args[6]
         z = args[7]

         # calling functions depending on which trigger id is sent
         for action in self.triggerActions[triggerID]:
            action(x, y, z)

      # OscIn addresses from Iannix that are listened for
      self.onInput("/transport", handleTransportMessage)
      self.onInput("/cursor", handleCursorMessage)
      self.onInput("/trigger", handleTriggerMessage)


   def onTrigger(self, triggerID, action):
      """Set up a function to call when a given trigger fires in the IanniX score.

      Args:
          triggerID (int or str): The ID of the trigger to listen for.
          action (Callable): The function to call; it receives three parameters, x, y, and z, the trigger's coordinates.
      """

      if triggerID in self.triggerActions.keys():
         self.triggerActions[triggerID].append(action)

      else:
         self.triggerActions[triggerID] = [action]


   def onCursor(self, cursorID, action):
      """Set up a function to call as a given cursor moves through the IanniX score.

      Args:
          cursorID (int or str): The ID of the cursor to listen for.
          action (Callable): The function to call; it receives three parameters, x, y, and z, the cursor's current coordinates.
      """

      if cursorID in self.cursorActions.keys():
         self.cursorActions[cursorID].append(action)

      else:
         self.cursorActions[cursorID] = [action]


   def onPlay(self, action):
      """Set up a function to call when IanniX starts playing.

      Args:
          action (Callable): The function to call; it receives one parameter, the current time in seconds.
      """

      self.transportActions["play"].append(action)


   def onStop(self, action):
      """Set up a function to call when IanniX stops.

      Args:
          action (Callable): The function to call; it receives one parameter, the current time in seconds.
      """

      self.transportActions["stop"].append(action)


   def onFastRewind(self, action):
      """Set up a function to call when IanniX fast-rewinds.

      Args:
          action (Callable): The function to call; it receives one parameter, the current time in seconds.
      """

      self.transportActions["fastrewind"].append(action)


class IannixOut(OscOut):
   """Send messages to a running IanniX application over OSC.

   IanniX is a graphic sequencer. Use an IannixOut to build its score (curves, points,
   triggers, and cursors) and to control playback. You can make several IannixOut objects
   to reach several IanniX installations. Extends OscOut.

   Args:
       ipAddress (str, optional): The IP address of the computer running IanniX. Defaults to this computer.
       port (int, optional): The port IanniX is listening on.
   """

   def __init__(self, ipAddress='127.0.0.1', port=57111):
      # initialize the OscOut IP Address and Port used by Iannix
      OscOut.__init__(self, ipAddress, port)

      # dictionary to keep count of what the next point ID should be;
      # <curveID> : <pointIDCounter>
      self.curvePointsID = {}

      # dictionary to keep track of what ids are in use and what each id is;
      # <objectID> : <type of object (e.g. "curve", "trigger", "cursor")
      self.objectIDs = {}


   def addPointToCurve(self, curveID, x=0.0, y=0.0, z=0.0, cx1=0.0, cy1=0.0, cz1=0.0, cx2=0.0, cy2=0.0, cz2=0.0):
      """Add a point to a curve in the IanniX score.

      The control points shape a quadratic Bezier curve between this point and the previous
      point on the curve.

      Args:
          curveID (int or str): The ID of the curve to add the point to.
          x (float, optional): The point's x coordinate.
          y (float, optional): The point's y coordinate.
          z (float, optional): The point's z coordinate.
          cx1 (float, optional): The x coordinate of the first Bezier control point.
          cy1 (float, optional): The y coordinate of the first Bezier control point.
          cz1 (float, optional): The z coordinate of the first Bezier control point.
          cx2 (float, optional): The x coordinate of the second Bezier control point.
          cy2 (float, optional): The y coordinate of the second Bezier control point.
          cz2 (float, optional): The z coordinate of the second Bezier control point.
      """

      # makes sure that the curve id exists
      if curveID not in self.objectIDs:
         raise ValueError("ID value", curveID, "does not exist.")

      # OSC messages to add a point to the curve
      self.sendMessage("/iannix/setPointAt", curveID, self.curvePointsID[curveID], x, y, z,
                       cx1, cy1, cz1, cx2, cy2, cz2)

      # increment the point id counter used for the curve
      self.curvePointsID[curveID]+= 1


   def addPointListToCurve(self, curveID, listPoints, listControlPoints1=None, listControlPoints2=None):
      """Add many points to a curve in the IanniX score at once.

      Each point is an (x, y, z) tuple. The two control-point lists shape the quadratic
      Bezier curves between points. Each control-point list must be either the same length as
      listPoints, or None to skip it.

      Args:
          curveID (int or str): The ID of the curve to add the points to.
          listPoints (list[tuple[float, float, float]]): The points to add, each an (x, y, z) tuple.
          listControlPoints1 (list[tuple[float, float, float]], optional): The first Bezier control point for each point, each a (cx1, cy1, cz1) tuple. Defaults to none.
          listControlPoints2 (list[tuple[float, float, float]], optional): The second Bezier control point for each point, each a (cx2, cy2, cz2) tuple. Defaults to none.
      """

      # makes sure that the curve id exists
      if curveID not in self.objectIDs:
         raise ValueError("ID value", curveID, "does not exist.")

      # creates lists of 0s if the listControlPoints are not used
      if listControlPoints1 is None:
          listControlPoints1 = [(0, 0, 0)] * len(listPoints)
      if listControlPoints2 is None:
          listControlPoints2 = [(0, 0, 0)] * len(listPoints)

      # make sure that all of the lists are the same length
      if not (len(listPoints) == len(listControlPoints1) == len(listControlPoints2)):
         raise ValueError("List lengths do not match.")

      # OSC messages in a for loop that add multiple points to a curve
      for i in range(len(listPoints)):
         x,   y,   z   = listPoints[i]
         cx1, cy1, cz1 = listControlPoints1[i]
         cx2, cy2, cz2 = listControlPoints2[i]

         self.sendMessage("/iannix/setPointAt", curveID, self.curvePointsID[curveID], x, y, z,
                          cx1, cy1, cz1, cx2, cy2, cz2)

         # increment the point id counter used for the curve
         self.curvePointsID[curveID]+= 1


   def addCurve(self, curveID, x, y, z):
      """Add a new curve to the IanniX score.

      The curve starts with no points. Add points to it with addPointToCurve() or
      addPointListToCurve().

      Args:
          curveID (int or str): The ID to give the new curve.
          x (float): The curve's x coordinate.
          y (float): The curve's y coordinate.
          z (float): The curve's z coordinate.
      """

      # makes sure that the curve id does not already exist
      if curveID in self.objectIDs:
         raise ValueError("ID value", curveID, "is currently taken.")

      # OSC messages needed to create a curve
      self.sendMessage("/iannix/add", "curve", curveID)
      self.sendMessage("/iannix/setpos", curveID, x, y, z)
      self.curvePointsID[curveID] = 0
      self.objectIDs[curveID] = "curve"


   def removeCurve(self, curveID):
      """Remove a curve from the IanniX score.

      Args:
          curveID (int or str): The ID of the curve to remove.
      """

      # make sure the ID exists
      if curveID not in self.objectIDs:
         raise ValueError("ID value", curveID, "does not exist.")

      # make sure that the ID is for a curve
      if self.objectIDs[curveID] != "curve":
         raise ValueError("ID value", curveID, "is not the ID of a curve.")

      # remove the curve
      self.sendMessage("/iannix/remove", curveID)

      # remove the curve from the list of object IDs in use
      del self.objectIDs[curveID]

      # remove the curve from the list of curve : point ids in use
      del self.curvePointsID[curveID]


   def addTrigger(self, triggerID, x, y, z):
      """Add a trigger to the IanniX score at the given coordinates.

      Args:
          triggerID (int or str): The ID to give the new trigger.
          x (float): The trigger's x coordinate.
          y (float): The trigger's y coordinate.
          z (float): The trigger's z coordinate.
      """

      # makes sure that the trigger id does not already exist
      if triggerID in self.objectIDs:
         raise ValueError("ID value", triggerID, "is currently taken.")

      # OSC messages needed to create a trigger
      self.sendMessage("/iannix/add", "trigger", triggerID)
      self.sendMessage("/iannix/setpos", triggerID, x, y, z)

      # adds the trigger to the dictionary of object ids
      self.objectIDs[triggerID] = "trigger"


   def removeTrigger(self, triggerID):
      """Remove a trigger from the IanniX score.

      Args:
          triggerID (int or str): The ID of the trigger to remove.
      """

      # make sure the ID exists
      if triggerID not in self.objectIDs:
         raise ValueError("ID value", triggerID, "does not exist.")

      # make sure that the ID is for a trigger
      if self.objectIDs[triggerID] != "trigger":
         raise ValueError("ID value", triggerID, "is not the ID of a trigger.")

      # remove the trigger
      self.sendMessage("/iannix/remove", triggerID)

      # remove the trigger from the list of object IDs in use
      del self.objectIDs[triggerID]


   def addCursor(self, curveID, cursorID, offset=0.0):
      """Add a cursor to a curve in the IanniX score.

      A cursor travels along its curve as the score plays.

      Args:
          curveID (int or str): The ID of the curve to place the cursor on.
          cursorID (int or str): The ID to give the new cursor.
          offset (float, optional): How far along the curve to start the cursor, in seconds from the start of the curve.
      """

      # make sure that the cursorID provided does not exist already
      if cursorID in self.objectIDs:
         raise ValueError("ID value", cursorID, "is currently taken.")

      # make sure that the curveID provided exists
      if curveID not in self.objectIDs:
         raise ValueError("ID value", curveID, "does not exist.")

      # make sure that the curveID provided is for a curve
      if self.objectIDs[curveID] != "curve":
         raise ValueError("ID value", curveID, "is not the ID of a curve.")

      # adds a cursor to a curve
      self.sendMessage("/iannix/add", "cursor", cursorID)
      self.sendMessage("/iannix/setcurve", cursorID, curveID)


   def removeCursor(self, cursorID):
      """Remove a cursor from the IanniX score.

      Args:
          cursorID (int or str): The ID of the cursor to remove.
      """

      # make sure the ID exists
      if cursorID not in self.objectIDs:
         raise ValueError("ID value", cursorID, "is not a valid ID.")

      # make sure that the ID is for a cursor
      if self.objectIDs[cursorID] != "cursor":
         raise ValueError("ID value", cursorID, "is not the ID of a cursor.")

      # remove the cursor
      self.sendMessage("/iannix/remove", cursorID)

      # remove the cursor from the list of object IDs in use
      del self.objectIDs[cursorID]


   def clear(self):
      """Remove every object from the IanniX score.
      """

      self.sendMessage("/iannix/clear")
      self.curvePointsID.clear()
      self.objectIDs.clear()


   def play(self):
      """Start the IanniX score playing.
      """

      self.sendMessage("/iannix/play")


   def stop(self):
      """Stop the IanniX score.
      """

      self.sendMessage("/iannix/stop")


   def fastRewind(self):
      """Fast-rewind the IanniX score.
      """

      self.sendMessage("/iannix/fastrewind")


################################################################################
# Unit Tests
################################################################################
if __name__ == '__main__':

   ############################################################################
   ### IannixIn Unit Tests ####################################################
   ############################################################################

   # define IannixIn object and variables that hold test IDs
   iannixIn = IannixIn(57110)
   triggerID = 3
   cursorID = 2

   ### test for onTrigger functionality #######################################
   def printOnTrigger(x, y, z):
      print("On Trigger Results", x, y, z)

   iannixIn.onTrigger(triggerID, printOnTrigger)

   ### test for onTrigger functionality #######################################
   def printOnCursor(x, y, z):
      print("On Cursor Results", x, y, z)

   iannixIn.onCursor(cursorID, printOnCursor)

   ### test for onPlay functionality ##########################################
   def printOnPlay(time):
      print("On Play Results:", time)

   iannixIn.onPlay(printOnPlay)

   ### test for onStop functionality ##########################################
   def printOnStop(time):
      print("On Stop Results:", time)

   iannixIn.onStop(printOnStop)

   ### test for onFastRewind functionality ####################################
   def printOnFastRewind(time):
      print("On FastRewind Results:", time)

   iannixIn.onFastRewind(printOnFastRewind)
