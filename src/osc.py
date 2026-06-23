#######################################################################################
# osc.py       Version 2.0     22-Jun-2026
#
# Taj Ballinger, Trevor Ritchie, Drew Smuniewski, and Bill Manaris
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
# This module provides OSC (Open Sound Control) input and output handling.
#
#######################################################################################
#
# REVISIONS:
#
# 2.0   22-Jun-2026 (tb)   Ported from JythonMusic to PythonMusic.
#      - Replaced JavaOSC backend with osc4py3
#      - OscIn runs its own background thread
#      - Ported OscMessage to a simple data wrapper
#      - Updated host-IP reporting to detect primary outbound IP and list alternative IPs
#      - Replaced JEM Stop-button cleanup (registerStopFunction) with atexit shutdown
#      - Added full Google-style docstrings throughout
#
#######################################################################################

from utilities import *    # mapValue, etc.
from osc4py3.as_eventloop import osc_startup, osc_terminate, osc_process, osc_send, osc_udp_client, osc_udp_server, osc_method
from osc4py3 import oscbuildparse, oscmethod
import threading
import socket
import time
import sys
import atexit
import re

##### Globals #########################################################################

_oscStarted   = False   # True once osc_startup() has been called
_activeOscIns = []      # tracks open OscIn objects for cleanup


def _getActiveIPs():
   """"""
   primary = "127.0.0.1"
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   try:
      # No packet is sent — connect() just selects the outbound interface so getsockname() works.
      sock.connect(("8.8.8.8", 80))
      primary = sock.getsockname()[0]
   except OSError:
      pass
   finally:
      sock.close()

   alternatives = []
   try:
      hostname = socket.gethostname()
      allIPs   = socket.gethostbyname_ex(hostname)[2]
      alternatives = sorted(set(ip for ip in allIPs if ip != "127.0.0.1" and ip != primary))
   except (socket.gaierror, OSError):
      pass

   return primary, alternatives


#################### OscIn ############################################################
#
# Receives OSC messages on a specified port.
#
# Usage:
#   oscIn = OscIn(57110)
#
#   def onMessage(message):
#      print(message.getAddress(), message.getArguments())
#
#   oscIn.onInput("/helloWorld", onMessage)   # call onMessage for /helloWorld messages
#   oscIn.onInput("*",          onMessage)   # call onMessage for all messages

ALL_MESSAGES = "/.*"   # matches all OSC addresses (Java 8 regex)

class OscIn:
   """Receive OSC messages from another device, such as a phone or tablet.

   OSC (Open Sound Control) is a way for programs and devices to send each other messages
   over a network. Creating an OscIn listens for messages on a port; use onInput() to call
   your own function whenever a message arrives at a given address.

   Args:
       port (int, optional): The port to listen on, a number from 1024 to 65535 that no other program is using.
   """

   def __init__(self, port=57110):
      global _oscStarted, _activeOscIns
      _activeOscIns.append(self)

      self._stopEvent = threading.Event()   # signals the processing thread to stop

      if not _oscStarted:
         osc_startup()
         _oscStarted = True

      self.port       = port
      hostIP, alternativeIPs = _getActiveIPs()
      self.ipAddress  = hostIP
      self.serverName = f"oscServer_{self.port}"

      osc_udp_server("0.0.0.0", self.port, self.serverName)

      print('OSC Server started:')
      print(f'Accepting OSC input on IP address {self.ipAddress}, at port {self.port}')
      if alternativeIPs:
         label = '(Alternative IP addresses: '
         print(f'{label}{alternativeIPs[0]}')
         for ip in alternativeIPs[1:]:
            print(f'{" " * len(label)}{ip}')
         print(f'{" " * (len(label) - 1)})')
      print('Use this info to configure OSC clients.\n')

      self.showIncomingMessages = True
      self._handlers = []   # [(compiled_regex, callback), ...]

      # Register a single catch-all handler; all pattern matching is done in _dispatch via Python regex.
      # "/*" covers single-level addresses (e.g. /note, /fader1). For deeper addresses (e.g. /a/b),
      # register additional patterns like "/*/*" explicitly.
      osc_method("/*", self._dispatch, argscheme=oscmethod.OSCARG_MESSAGE)

      self._processThread = threading.Thread(target=self._processingLoop, daemon=True)
      self._processThread.start()


   def __str__(self):
      return f'OscIn(port = {self.port})'


   def __repr__(self):
      return str(self)


   def onInput(self, oscAddress, action):
      """Set up a function to call when a message arrives at a given address.

      An OSC address looks like a URL, for example "/first/second/third". The address may
      also be a pattern, to match several addresses at once.

      Args:
          oscAddress (str): The OSC address to listen for, for example "/first/second/third".
          action (Callable): The function to call; it receives one parameter, the incoming OscMessage.
      """
      self._handlers.append((re.compile(oscAddress), action))


   def _dispatch(self, rawMsg):
      """"""
      address = rawMsg.addrpattern
      msg     = OscMessage(address, rawMsg.arguments)

      if self.showIncomingMessages:
         self._printIncomingMessage(msg)

      for pattern, callback in self._handlers:
         if re.fullmatch(pattern, address):
            self._executeCallback(callback, msg)


   def showMessages(self):
      """Start printing incoming OSC messages to the console.

      This is the default, and is handy for discovering what messages a device sends.
      """
      self.showIncomingMessages = True


   def hideMessages(self):
      """Stop printing incoming OSC messages to the console.
      """
      self.showIncomingMessages = False


   def _printIncomingMessage(self, message):
      """"""
      oscAddress = message.getAddress()
      oscArgs    = message.getArguments()

      print(f'OSC In - Address: "{oscAddress}"', end='')
      for i, arg in enumerate(oscArgs):
         if isinstance(arg, str):
            print(f' , Argument {i}: "{arg}"', end='')
         else:
            print(f' , Argument {i}: {arg}', end='')
      print()


   def _executeCallback(self, handler, message):
      """"""
      try:
         handler(message)
      except Exception as e:
         print(f"OscIn: Error executing callback: {e}")


   def _processingLoop(self):
      """"""
      try:
         while not self._stopEvent.is_set():
            osc_process()
            time.sleep(0.001)
      except Exception as e:
         print(f"[OSC Error] OscIn on port {self.port} encountered an error: {e}", file=sys.stderr)


#################### OscOut ###########################################################
#
# Sends OSC messages to a specified IP address and port.
#
# Usage:
#   oscOut = OscOut("localhost", 57110)
#   oscOut.sendMessage("/helloWorld")
#   oscOut.sendMessage("/itsFullOfStars", 1, 2.3, "wow!", True)

class OscOut:
   """Send OSC messages to another device, such as a phone or tablet.

   OSC (Open Sound Control) is a way for programs and devices to send each other messages
   over a network. Creating an OscOut connects to a device at an IP address and port; use
   sendMessage() to send it messages. You can make several OscOut objects to reach several
   devices.

   Args:
       ipAddress (str, optional): The device's IP address, for example "192.168.1.223". Use "localhost" for a program on this same computer.
       port (int, optional): The port the device is listening on, a number from 1024 to 65535.
   """

   def __init__(self, ipAddress='localhost', port=57110):
      global _oscStarted

      if not _oscStarted:
         osc_startup()
         _oscStarted = True

      if ipAddress == "localhost":
         ipAddress = "127.0.0.1"

      self.ipAddress     = ipAddress
      self.port   = port
      self.client = f"oscClient_{self.ipAddress}_{self.port}"

      osc_udp_client(self.ipAddress, self.port, self.client)


   def __str__(self):
      return f'OscOut(ipAddress = {self.ipAddress}, port = {self.port})'


   def __repr__(self):
      return str(self)


   def sendMessage(self, oscAddress, *args):
      """Send an OSC message to the connected device.

      A message is an address plus any number of arguments.

      Args:
          oscAddress (str): The OSC address to send to, for example "/first/second/third".
          *args: Zero or more values to send with the message (numbers, text, or True/False).
      """
      message = oscbuildparse.OSCMessage(oscAddress, None, args)
      osc_send(message, self.client)
      osc_process()


#################### OscMessage #######################################################

class OscMessage:
   """Hold an OSC message: an address and its arguments.

   You normally receive an OscMessage rather than build one. An OscMessage is what the
   function you set up with OscIn.onInput() is handed. Read the message with getAddress()
   and getArguments(). The main reason to build one yourself is to test such a callback.
   To send a message, use OscOut.sendMessage(), which builds and sends one for you.
   OscOut.sendMessage() does not take an OscMessage.

   Args:
       oscAddress (str): The OSC address, for example "/first/second/third".
       arguments (list, optional): The message's arguments (numbers, text, or True/False). Defaults to no arguments.
   """

   def __init__(self, oscAddress, arguments=None):
      self.oscAddress = oscAddress

      if arguments is None:   # address-only message (no arguments)
         self.arguments = []
      else:
         self.arguments = list(arguments)   # copy, so later changes to the caller's list don't leak in


   def __str__(self):
      return f'OscMessage(oscAddress = {self.oscAddress}, args = {self.arguments})'


   def __repr__(self):
      return str(self)


   def getAddress(self):
      """Return the message's OSC address.

      Returns:
          oscAddress (str): The OSC address, for example "/first/second/third".
      """
      oscAddress = self.oscAddress
      return oscAddress


   def getArguments(self):
      """Return the message's arguments.

      Returns:
          argumentsList (list): The message's arguments (numbers, text, or True/False), in order.
      """
      argumentsList = self.arguments
      return argumentsList


##### Cleanup #########################################################################

def _cleanupOsc():
   """"""
   global _activeOscIns

   for instance in list(_activeOscIns):
      if hasattr(instance, '_processThread') and instance._processThread.is_alive():
         instance._stopEvent.set()
         instance._processThread.join(timeout=2.0)   # wait up to 2s for clean shutdown

   if _oscStarted:
      try:
         osc_terminate()
      except Exception as e:
         print(f"[OSC Cleanup Error] {e}", file=sys.stderr)

atexit.register(_cleanupOsc)

#######################################################################################
# Tests
#######################################################################################

if __name__ == "__main__":
   pass
