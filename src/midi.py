#######################################################################################
# midi.py       Version 3.0     01-Apr-2026
#
# Taj Ballinger, Trevor Ritchie, and Bill Manaris
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
# This module provides MIDI input and output device handling.
#
#######################################################################################
#
# REVISIONS:
#
# 3.0   01-Apr-2026 (tr)   Ported from JythonMusic to PythonMusic.
#      - Replaced javax.sound.midi backend with mido
#      - MidiIn now reads input on its own background polling thread
#      - Expanded incoming-message handling to controller, pitch-bend, aftertouch,
#        poly-touch, system, and realtime events, with matching event-type constants
#      - int pitches now play as plain MIDI notes; only float frequencies use pitch bend
#      - Replaced JEM Stop-button cleanup (registerStopFunction) with atexit shutdown
#      - Added full Google-style docstrings throughout
#
#######################################################################################

from utilities import *    # mapValue, etc.
import mido                   # MIDI input/output and message handling
from timer import Timer       # for scheduling MIDI events
from music import freqToNote, mapValue, Note, Phrase, Part, Score, REST  # music data structures and utilities
import atexit                 # ensures cleanup of MIDI resources on program exit
import threading              # for MidiIn polling thread
import time                   # for polling sleep interval

##### Constants #######################################################################
# MIDI event type constants
ALL_EVENTS     = -1   # register a callback for all event types
NOTE_ON        = 144  # 0x90 - Note On
NOTE_OFF       = 128  # 0x80 - Note Off
SET_INSTRUMENT = 192  # 0xC0 - Program Change (set instrument)
CONTROL_CHANGE = 176  # 0xB0 - Control Change
PITCH_BEND     = 224  # 0xE0 - Pitch Bend
AFTERTOUCH     = 208  # 0xD0 - Aftertouch
POLYTOUCH      = 160  # 0xA0 - Polyphonic Aftertouch

# system common and real-time message type values
SYSTEM_MESSAGE_VALUES = {
   'system_reset':     255,   # 0xFF - System Reset
   'system_exclusive': 240,   # 0xF0 - System Exclusive
   'songpos':          242,   # 0xF2 - Song Position Pointer
   'songsel':          243,   # 0xF3 - Song Select
   'tune_request':     246    # 0xF6 - Tune Request
}

REALTIME_MESSAGE_VALUES = {
   'clock':    248,   # 0xF8 - Timing Clock
   'start':    250,   # 0xFA - Start
   'continue': 251,   # 0xFB - Continue
   'stop':     252    # 0xFC - Stop
}

# Pitch bend range: 0 = max downward, 16383 = max upward, 8192 = center (no bend).
PITCHBEND_MIN    = 0
PITCHBEND_MAX    = 16383
PITCHBEND_NORMAL = 8192

##### Globals #########################################################################
_activeMidiInObjects  = []   # tracks open MidiIn objects for cleanup
_activeMidiOutObjects = []   # tracks open MidiOut objects for cleanup

notesCurrentlyPlaying = []   # (pitch, channel) tuples; prevents early note-off for overlapping notes


#################### MidiIn ###########################################################
#
# Receives MIDI input from a connected device.
#
# Usage:
#   midiIn = MidiIn()
#
#   def onEvent(eventType, channel, data1, data2):
#      print(eventType, channel, data1, data2)
#
#   midiIn.onInput(ALL_EVENTS, onEvent)

class MidiIn:
   """Receive MIDI messages from an input device, such as a keyboard or controller.

   Creating a MidiIn connects to an input MIDI device. If you do not name one, or the
   named one is unavailable, a window opens for you to pick from the devices found. Once
   connected, use the on… methods to run your own functions when notes are played,
   released, or the instrument is changed.

   Args:
       preferredDevice (str, optional): The name of the input device to connect to. If omitted or unavailable, a selection window opens.
   """

   def __init__(self, preferredDevice=''):
      self.preferredDevice      = preferredDevice   # device to open automatically (if available)
      self.display              = None              # device-selection GUI (shown when needed)
      self.waitingToSetup       = True              # True until a device is selected
      self.midiDevice           = None              # selected MIDI device
      self.midiDeviceName       = None              # display name of selected device
      self.showIncomingMessages = True              # print incoming messages to console
      self.eventHandlers        = {}                # {eventType: [callbacks]}
      self._port                = None              # mido port object
      self._stopEvent           = threading.Event() # signals the polling thread to stop
      self._pollThread          = None              # background thread for polling MIDI input

      self.selectMidiInput(self.preferredDevice)


   def __str__(self):
      return f'MidiIn(preferredDevice = {self.preferredDevice})'


   def __repr__(self):
      return str(self)


   def selectMidiInput(self, preferredDevice=''):
      """Connect to a preferred input MIDI device, or open a window to pick one.

      If the named device is not available, a window opens listing the input devices found.

      Args:
          preferredDevice (str, optional): The name of the input device to connect to. If omitted or unavailable, a selection window opens.
      """
      self.preferredDevice = preferredDevice

      availablePorts = mido.get_input_names()
      self.inputDevices = {}

      for port in availablePorts:
         self.inputDevices[port] = port

      if self.preferredDevice in self.inputDevices:
         self.openInputDevice(self.preferredDevice)

      else:
         items = sorted(self.inputDevices.keys())

         if items:
            from gui import Display, DropDownList, Color

            self.display = Display("Select MIDI Input", 400, 125)
            self.display.drawLabel('Select a MIDI input device from the list', 45, 30)

            deviceDropdown = DropDownList(items, self.openInputDevice)
            self.display.add(deviceDropdown, 40, 50)
            self.display.setColor( Color(124, 201, 251) )

            # Block until the user picks a device (callback on listener thread clears this)
            while self.waitingToSetup:
               time.sleep(0.01)

         else:
            print("MidiIn: No available MIDI input devices. Please connect a device.")


   def openInputDevice(self, selectedItem):
      """Open a named input MIDI device.

      This is the callback used by the device-selection window; you do not normally call it
      yourself.

      Args:
          selectedItem (str): The name of the input device to open.
      """
      global _activeMidiInObjects

      try:
         print(f'MIDI input device set to "{selectedItem}".')
         deviceInfo = self.inputDevices[selectedItem]

         self.midiDeviceName = selectedItem
         self._port = mido.open_input(deviceInfo)
         self.waitingToSetup = False

         self._stopEvent.clear()
         self._pollThread = threading.Thread(target=self._pollingLoop, daemon=True)
         self._pollThread.start()

         if self.display:
            self.display.close()

         _activeMidiInObjects.append(self)

      except Exception as e:
         print(f"Error opening MIDI device: {e}")


   def close(self):
      """Close the input device and free its resources.

      Also clears every event handler set with the on… methods.
      """
      self._stopEvent.set()
      if self._pollThread and self._pollThread.is_alive():
         self._pollThread.join(timeout=2.0)

      if self._port:
         self._port.close()
         self._port = None

      if self in _activeMidiInObjects:
         _activeMidiInObjects.remove(self)


   def onNoteOn(self, action):
      """Set up a function to call whenever a note is played on the device.

      Args:
          action (Callable): The function to call; it receives four parameters: eventType (144), channel (0 to 15), data1 (the pitch, 0 to 127), and data2 (the velocity, 0 to 127).
      """
      if NOTE_ON not in self.eventHandlers:
         self.eventHandlers[NOTE_ON] = []
      self.eventHandlers[NOTE_ON].append(action)


   def onNoteOff(self, action):
      """Set up a function to call whenever a note is released on the device.

      Args:
          action (Callable): The function to call; it receives four parameters: eventType (128), channel (0 to 15), data1 (the pitch, 0 to 127), and data2 (unused).
      """
      if NOTE_OFF not in self.eventHandlers:
         self.eventHandlers[NOTE_OFF] = []
      self.eventHandlers[NOTE_OFF].append(action)


   def onSetInstrument(self, action):
      """Set up a function to call whenever the instrument is changed on the device.

      Args:
          action (Callable): The function to call; it receives four parameters: eventType (192), channel (0 to 15), data1 (the new instrument, 0 to 127), and data2 (unused).
      """
      if SET_INSTRUMENT not in self.eventHandlers:
         self.eventHandlers[SET_INSTRUMENT] = []
      self.eventHandlers[SET_INSTRUMENT].append(action)


   def onInput(self, eventType, action):
      """Set up a function to call for a particular kind of MIDI event.

      Call this again with different event types to handle each kind separately (one
      function per event type). Using ALL_EVENTS catches every event not already handled.

      Args:
          eventType (int): The MIDI event type to handle, or ALL_EVENTS for anything not handled.
          action (Callable): The function to call; it receives four parameters: eventType, channel, data1, and data2.
      """
      if eventType not in self.eventHandlers:
         self.eventHandlers[eventType] = []
      self.eventHandlers[eventType].append(action)


   def showMessages(self):
      """Start printing incoming MIDI messages to the console.

      This is the default, and is handy for discovering what messages a device sends.
      """
      self.showIncomingMessages = True


   def hideMessages(self):
      """Stop printing incoming MIDI messages to the console.
      """
      self.showIncomingMessages = False


   def _pollingLoop(self):
      """"""
      while not self._stopEvent.is_set():
         if self._port:
            for message in self._port.iter_pending():
               self._handleMidiMessage(message)
         time.sleep(0.001)


   def _handleMidiMessage(self, message):
      """"""
      msgType    = None
      msgChannel = 0
      msgData1   = 0
      msgData2   = 0

      if message.type == 'note_on':
         msgType    = NOTE_ON
         msgChannel = message.channel
         msgData1   = message.note
         msgData2   = message.velocity
         if msgData2 == 0:               # velocity 0 means note off (per MIDI spec)
            msgType = NOTE_OFF

      elif message.type == 'note_off':
         msgType    = NOTE_OFF
         msgChannel = message.channel
         msgData1   = message.note
         msgData2   = message.velocity

      elif message.type == 'program_change':
         msgType    = SET_INSTRUMENT
         msgChannel = message.channel
         msgData1   = message.program
         msgData2   = 0

      elif message.type == 'control_change':
         msgType    = CONTROL_CHANGE
         msgChannel = message.channel
         msgData1   = message.control
         msgData2   = message.value

      elif message.type == 'pitchwheel':
         msgType     = PITCH_BEND
         msgChannel  = message.channel
         pitch_value = message.pitch + 8192      # convert mido's -8192..8191 to 0..16383
         msgData1    = pitch_value & 0x7F        # LSB
         msgData2    = (pitch_value >> 7) & 0x7F # MSB

      elif message.type == 'aftertouch':
         msgType    = AFTERTOUCH
         msgChannel = message.channel
         msgData1   = message.value
         msgData2   = 0

      elif message.type == 'polytouch':
         msgType    = POLYTOUCH
         msgChannel = message.channel
         msgData1   = message.note
         msgData2   = message.value

      elif message.type == 'sysex':
         msgType    = 240
         msgChannel = 0
         msgData1   = 0
         msgData2   = 0

      elif message.type.startswith('system_'):
         msgType    = SYSTEM_MESSAGE_VALUES.get(message.type, 240)
         msgChannel = 0
         msgData1   = getattr(message, 'data1', 0)
         msgData2   = getattr(message, 'data2', 0)

      elif message.type in ('clock', 'start', 'continue', 'stop'):
         msgType    = REALTIME_MESSAGE_VALUES.get(message.type, 248)
         msgChannel = 0
         msgData1   = 0
         msgData2   = 0

      if msgType is not None:
         if self.showIncomingMessages:
            print(f"{self.midiDeviceName} (MidiIn) - Event Type: {msgType}, Channel: {msgChannel}, Data 1: {msgData1}, Data 2: {msgData2}")

         for handler in self.eventHandlers.get(msgType, []):
            try:
               self._executeCallback(handler, msgType, msgChannel, msgData1, msgData2)
            except Exception as e:
               print(f"Error executing MIDI event handler: {e}")

         for handler in self.eventHandlers.get(ALL_EVENTS, []):
            try:
               self._executeCallback(handler, msgType, msgChannel, msgData1, msgData2)
            except Exception as e:
               print(f"Error executing MIDI event handler: {e}")


   def _executeCallback(self, handler, msgType, msgChannel, msgData1, msgData2):
      """"""
      try:
         handler(msgType, msgChannel, msgData1, msgData2)
      except Exception as e:
         print(f"MidiIn: Error executing callback: {e}")


#################### MidiOut ##########################################################
#
# Sends MIDI output to a connected device.
#
# Usage:
#   midiOut = MidiOut()
#   midiOut.sendMidiMessage(NOTE_ON, channel, pitch, velocity)
#   midiOut.sendMidiMessage(NOTE_OFF, channel, pitch, 0)

class MidiOut:
   """Send MIDI messages to an output device or synthesizer.

   Creating a MidiOut connects to an output MIDI device. If you do not name one, or the
   named one is unavailable, a window opens for you to pick from the devices found. Once
   connected, you can play music library material, start and stop individual notes and
   frequencies, and set each channel's instrument, volume, and panning.

   Args:
       preferredDevice (str, optional): The name of the output device to connect to. If omitted or unavailable, a selection window opens.
   """

   def __init__(self, preferredDevice=''):
      self.preferredDevice = preferredDevice
      self.display         = None    # device-selection GUI (shown when needed)
      self.waitingToSetup  = True    # True until a device is selected
      self.midiDevice      = None    # selected MIDI device
      self.midiDeviceName  = None    # display name of selected device
      self._port           = None    # mido port object

      self.instrument = {}   # current instrument per channel
      self.volume     = {}   # current volume per channel
      self.panning    = {}   # current panning per channel
      self.pitchBend  = {}   # current pitch bend per channel

      for channel in range(16):
         self.instrument[channel] = 0    # PIANO (default)
         self.volume[channel]     = 127  # max volume
         self.panning[channel]    = 63   # center
         self.pitchBend[channel]  = 0    # no bend

      self.selectMidiOutput(self.preferredDevice)


   def __str__(self):
      return f'MidiOut(preferredDevice = {self.preferredDevice})'

   def __repr__(self):
      return str(self)


   def close(self):
      """Close the output device.

      On some systems a device, once closed, cannot be reopened.
      """
      self.allNotesOff()

      if self._port:
         self._port.close()
         self._port = None

      if self in _activeMidiOutObjects:
         _activeMidiOutObjects.remove(self)


   def play(self, material):
      """Play music library material through the output device.

      Works like Play.midi().

      Args:
          material (Note, Phrase, Part, or Score): The music to play.
      """
      # do necessary datatype wrapping (we need a Score to traverse parts/phrases/notes)
      if isinstance(material, Note):
         material = Phrase(material)
      if isinstance(material, Phrase):   # no elif - we need to successively wrap from Note to Score
         material = Part(material)
         material.setInstrument(-1)     # indicate no default instrument (needed to access per-channel instrument)
      if isinstance(material, Part):     # no elif - we need to successively wrap from Note to Score
         material = Score(material)
      if not isinstance(material, Score):
         print(f'MidiOut.play(): Unrecognized type {type(material)}, expected Note, Phrase, Part, or Score.')
         return

      score = material

      # collect all non-REST notes with absolute ms start times
      noteList = []
      tempo = score.getTempo()
      for part in score.getPartList():
         channel    = part.getChannel()
         instrument = self.getInstrument(channel)
         if part.getInstrument() > -1:   # part instrument overrides channel default
            instrument = part.getInstrument()
         if part.getTempo() > -1:        # part tempo overrides score tempo
            tempo = part.getTempo()
         for phrase in part.getPhraseList():
            if phrase.getInstrument() > -1:   # phrase instrument overrides part instrument
               instrument = phrase.getInstrument()
            if phrase.getTempo() > -1:        # phrase tempo overrides part tempo
               tempo = phrase.getTempo()

            FACTOR    = 1000 * 60.0 / tempo   # convert quarter-note units → milliseconds
            startTime = phrase.getStartTime() * FACTOR

            for note in phrase.getNoteList():
               frequency = note.getFrequency()
               panning   = mapValue(note.getPan(), 0.0, 1.0, 0, 127)   # map 0.0–1.0 → 0–127
               start     = int(startTime)
               duration  = int(note.getLength() * FACTOR)
               startTime += note.getDuration() * FACTOR
               dynamic   = note.getDynamic()

               if frequency != REST:
                  noteList.append((start, duration, frequency, dynamic, channel, instrument, panning))

      # sort by start time so chords (same start time, duration=0) sort before their anchor note
      noteList.sort()

      # schedule all notes; chords are sequences of duration=0 notes followed by one note with the real duration
      chordNotes = []
      for start, duration, pitch, dynamic, channel, instrument, panning in noteList:
         self.setInstrument(instrument, channel)

         if duration == 0:   # chord member — collect it
            chordNotes.append([start, duration, pitch, dynamic, channel, panning])

         elif chordNotes == []:   # regular solo note
            self.note(pitch, start, duration, dynamic, channel, panning)

         else:   # final note of a chord — schedule all collected chord members with this duration
            chordNotes.append([start, duration, pitch, dynamic, channel, panning])
            for start, _, pitch, dynamic, channel, panning in chordNotes:
               self.note(pitch, start, duration, dynamic, channel, panning)
            chordNotes = []


   def noteOn(self, pitch, dynamic=100, channel=0, panning=-1):
      """Start a pitch sounding on the device, and leave it sounding.

      The note keeps playing until you stop it with noteOff().

      Args:
          pitch (int or float): A MIDI pitch from 0 to 127, or a frequency in hertz (8.17 to 12600.0) to reach pitches between the standard notes.
          dynamic (int, optional): How loud the note is, from 0 to 127.
          channel (int, optional): The channel to play on, from 0 to 15.
          panning (int, optional): Stereo position from 0 (left) to 127 (right); -1 uses the global panning.
      """

      if isinstance(pitch, int) and (0 <= pitch <= 127):
         if panning != -1:
            self.sendMidiMessage(CONTROL_CHANGE, channel, 10, panning)
         self.sendMidiMessage(NOTE_ON, channel, pitch, dynamic)
         notesCurrentlyPlaying.append((pitch, channel))

      elif isinstance(pitch, float):
         self.frequencyOn(pitch, dynamic, channel, panning)

      else:
         print(f"MidiOut.noteOn(): Unrecognized pitch {pitch}, expected int 0-127 or float Hz 8.17-12600.0.")


   def frequencyOn(self, frequency, dynamic=100, channel=0, panning=-1):
      """Start a frequency sounding on the device, and leave it sounding.

      Stop it with frequencyOff(). Play only one frequency per channel at a time: since this
      uses pitch bend, it affects every other note sounding on the channel.

      Args:
          frequency (float): The frequency to play, in hertz (8.17 to 12600.0).
          dynamic (int, optional): How loud the note is, from 0 to 127.
          channel (int, optional): The channel to play on, from 0 to 15.
          panning (int, optional): Stereo position from 0 (left) to 127 (right); -1 uses the global panning.
      """
      if isinstance(frequency, float) and (8.17 <= frequency <= 12600.0):
         pitch, bend = freqToNote(frequency)
         notesCurrentlyPlaying.append((pitch, channel))
         self.noteOnPitchBend(pitch, bend, dynamic, channel, panning)
      else:
         print(f"MidiOut.frequencyOn(): Invalid frequency {frequency}, expected float Hz 8.17-12600.0.")


   def noteOff(self, pitch, channel=0):
      """Stop a pitch from sounding on the device.

      If the pitch is not sounding on this channel, nothing happens.

      Args:
          pitch (int or float): A MIDI pitch from 0 to 127, or a frequency in hertz (8.17 to 12600.0).
          channel (int, optional): The channel it is playing on, from 0 to 15.
      """

      if isinstance(pitch, int) and (0 <= pitch <= 127):
         noteID = (pitch, channel)
         if noteID in notesCurrentlyPlaying:
            notesCurrentlyPlaying.remove(noteID)
            if noteID not in notesCurrentlyPlaying:   # only send if no more instances are playing
               self.sendMidiMessage(NOTE_OFF, channel, pitch, 0)

      elif isinstance(pitch, float):
         self.frequencyOff(pitch, channel)

      else:
         print(f"MidiOut.noteOff(): Unrecognized pitch {pitch}, expected int 0-127 or float Hz 8.17-12600.0.")


   def frequencyOff(self, frequency, channel=0):
      """Stop a frequency from sounding on the device.

      If the frequency is not sounding on this channel, nothing happens.

      Args:
          frequency (float): The frequency to stop, in hertz (8.17 to 12600.0).
          channel (int, optional): The channel it is playing on, from 0 to 15.
      """
      if isinstance(frequency, float) and (8.17 <= frequency <= 12600.0):
         pitch, _ = freqToNote(frequency)
         noteID = (pitch, channel)

         if noteID in notesCurrentlyPlaying:
            notesCurrentlyPlaying.remove(noteID)
            if noteID not in notesCurrentlyPlaying:
               self.sendMidiMessage(NOTE_OFF, channel, pitch, 0)
         else:
            print(f"MidiOut.frequencyOff(): Frequency {frequency} Hz (pitch {pitch}) on channel {channel} is not currently playing.")

      else:
         print(f"MidiOut.frequencyOff(): Invalid frequency {frequency}, expected float Hz 8.17-12600.0.")


   def note(self, pitch, start, duration, dynamic=100, channel=0, panning=-1):
      """Schedule a note on the device to play after a delay and last a set time.

      Args:
          pitch (int): A MIDI pitch, from 0 to 127.
          start (int or float): How long from now the note begins, in milliseconds.
          duration (int or float): How long the note lasts, in milliseconds.
          dynamic (int, optional): How loud the note is, from 0 to 127.
          channel (int, optional): The channel to play on, from 0 to 15.
          panning (int, optional): Stereo position from 0 (left) to 127 (right); -1 uses the global panning.
      """
      Timer(start,          self.noteOn,  [pitch, dynamic, channel, panning], False).start()
      Timer(start+duration, self.noteOff, [pitch, channel],                   False).start()


   def frequency(self, frequency, start, duration, dynamic=100, channel=0, panning=-1):
      """Schedule a frequency on the device to play after a delay and last a set time.

      Play only one frequency per channel at a time: since this uses pitch bend, it affects
      every other note sounding on the channel.

      Args:
          frequency (float): The frequency to play, in hertz (8.17 to 12600.0).
          start (int or float): How long from now the note begins, in milliseconds.
          duration (int or float): How long the note lasts, in milliseconds.
          dynamic (int, optional): How loud the note is, from 0 to 127.
          channel (int, optional): The channel to play on, from 0 to 15.
          panning (int, optional): Stereo position from 0 (left) to 127 (right); -1 uses the global panning.
      """
      Timer(start,          self.frequencyOn,  [frequency, dynamic, channel, panning], False).start()
      Timer(start+duration, self.frequencyOff, [frequency, channel],                   False).start()


   def setPitchBend(self, bend=0, channel=0):
      """Set the pitch bend for a channel, used for notes played next.

      Args:
          bend (int, optional): How far to bend the pitch, in pitch bend units from -8191 (full down) to 8192 (full up), where 0 means no bend.
          channel (int, optional): The channel to set, from 0 to 15.
      """
      self.pitchBend[channel] = bend

      midiBend = max(PITCHBEND_MIN, min(bend + PITCHBEND_NORMAL, PITCHBEND_MAX))
      lsb = midiBend & 0x7F
      msb = (midiBend >> 7) & 0x7F

      self.sendMidiMessage(PITCH_BEND, channel, lsb, msb)


   def getPitchBend(self, channel=0):
      """Return the current pitch bend for a channel.

      Args:
          channel (int, optional): The channel to read, from 0 to 15.

      Returns:
          pitchBend (int): The current bend, in pitch bend units from -8191 to 8192, where 0 means no bend.
      """
      pitchBend = self.pitchBend[channel]
      return pitchBend


   def noteOnPitchBend(self, pitch, bend=0, dynamic=100, channel=0, panning=-1):
      """Start a pitch sounding on the device with a pitch bend, and leave it sounding.

      Stop it with noteOff().

      Args:
          pitch (int): A MIDI pitch, from 0 to 127.
          bend (int, optional): How far to bend the pitch, in pitch bend units from -8191 (full down) to 8192 (full up), where 0 means no bend.
          dynamic (int, optional): How loud the note is, from 0 to 127.
          channel (int, optional): The channel to play on, from 0 to 15.
          panning (int, optional): Stereo position from 0 (left) to 127 (right); -1 uses the global panning.
      """
      self.setPitchBend(bend, channel)
      if panning != -1:
         self.sendMidiMessage(CONTROL_CHANGE, channel, 10, panning)
      self.sendMidiMessage(NOTE_ON, channel, pitch, dynamic)


   def allNotesOff(self):
      """Stop every note from sounding, on all channels.
      """
      self.allFrequenciesOff()


   def allFrequenciesOff(self):
      """Stop every frequency from sounding, on all channels.

      Same as allNotesOff(), and also resets pitch bend on every channel.
      """
      for channel in range(16):
         self.sendMidiMessage(CONTROL_CHANGE, channel, 123, 0)
         self.setPitchBend(0, channel)


   def stop(self):
      """Stop all MIDI music on the device from sounding.
      """
      self.allNotesOff()


   def setInstrument(self, instrument, channel=0):
      """Set the instrument for a channel.

      Notes played on this channel will sound using this instrument.

      Args:
          instrument (int): The instrument (timbre), as a MIDI instrument number from 0 to 127.
          channel (int, optional): The channel to set, from 0 to 15.
      """
      self.instrument[channel] = instrument
      self.sendMidiMessage(SET_INSTRUMENT, channel, instrument, 0)


   def getInstrument(self, channel=0):
      """Return the instrument set for a channel.

      Args:
          channel (int, optional): The channel to read, from 0 to 15.

      Returns:
          instrument (int): The instrument (timbre), as a MIDI instrument number from 0 to 127.
      """
      instrument = self.instrument[channel]
      return instrument


   def setVolume(self, volume, channel=0):
      """Set the main volume for a channel.

      This is the channel's overall volume, separate from how loud each note is played
      (see noteOn()).

      Args:
          volume (int): The main volume, from 0 to 127.
          channel (int, optional): The channel to set, from 0 to 15.
      """
      self.volume[channel] = volume
      self.sendMidiMessage(CONTROL_CHANGE, channel, 7, volume)


   def getVolume(self, channel=0):
      """Return the main volume for a channel.

      Args:
          channel (int, optional): The channel to read, from 0 to 15.

      Returns:
          volume (int): The main volume, from 0 to 127.
      """
      volume = self.volume[channel]
      return volume


   def setPanning(self, panning, channel=0):
      """Set the main stereo position for a channel.

      The default is the middle (64). Note that this does not affect a score played through
      play().

      Args:
          panning (int): Stereo position from 0 (left) through 64 (center) to 127 (right).
          channel (int, optional): The channel to set, from 0 to 15.
      """
      self.panning[channel] = panning
      self.sendMidiMessage(CONTROL_CHANGE, channel, 10, panning)


   def getPanning(self, channel=0):
      """Return the main stereo position for a channel.

      Args:
          channel (int, optional): The channel to read, from 0 to 15.

      Returns:
          panning (int): Stereo position from 0 (left) through 64 (center) to 127 (right).
      """
      panning = self.panning[channel]
      return panning


   def sendMidiMessage(self, eventType, channel, data1, data2):
      """Send a raw MIDI message to the device.

      For messages the other methods do not cover. See the MIDI standard, or your
      synthesizer's documentation, for the meaning of each value.

      Args:
          eventType (int): The MIDI event type.
          channel (int): The MIDI channel, from 0 to 15.
          data1 (int): The first data byte; its meaning depends on the event type.
          data2 (int): The second data byte; its meaning depends on the event type.
      """
      try:
         if eventType == NOTE_ON:
            msg = mido.Message('note_on', channel=channel, note=data1, velocity=data2)

         elif eventType == NOTE_OFF:
            msg = mido.Message('note_off', channel=channel, note=data1, velocity=data2)

         elif eventType == SET_INSTRUMENT:
            msg = mido.Message('program_change', channel=channel, program=data1)

         elif eventType == CONTROL_CHANGE:
            msg = mido.Message('control_change', channel=channel, control=data1, value=data2)

         elif eventType == PITCH_BEND:
            # Recombine 7-bit LSB/MSB into a 14-bit value, then shift to mido's -8192..8191 range.
            bendValue = ((data2 << 7) + data1) - PITCHBEND_NORMAL
            msg = mido.Message('pitchwheel', channel=channel, pitch=bendValue)

         elif eventType == AFTERTOUCH:
            msg = mido.Message('aftertouch', channel=channel, value=data1)

         elif eventType == POLYTOUCH:
            msg = mido.Message('polytouch', channel=channel, note=data1, value=data2)

         elif eventType == SYSTEM_MESSAGE_VALUES['system_exclusive']:
            msg = mido.Message('sysex', data=[data1, data2])

         elif eventType == SYSTEM_MESSAGE_VALUES['songpos']:
            msg = mido.Message('songpos', pos=(data2 << 7) + data1)

         elif eventType == SYSTEM_MESSAGE_VALUES['songsel']:
            msg = mido.Message('songsel', song=data1)

         elif eventType == SYSTEM_MESSAGE_VALUES['tune_request']:
            msg = mido.Message('tune_request')

         elif eventType == SYSTEM_MESSAGE_VALUES['system_reset']:
            msg = mido.Message('reset')

         elif eventType == REALTIME_MESSAGE_VALUES['clock']:
            msg = mido.Message('clock')

         elif eventType == REALTIME_MESSAGE_VALUES['start']:
            msg = mido.Message('start')

         elif eventType == REALTIME_MESSAGE_VALUES['continue']:
            msg = mido.Message('continue')

         elif eventType == REALTIME_MESSAGE_VALUES['stop']:
            msg = mido.Message('stop')

         else:
            print(f"Unsupported MIDI message type: {eventType}")
            return

         if self._port:
            self._port.send(msg)

      except Exception as e:
         print(f"Error sending MIDI message: {e}")


   def selectMidiOutput(self, preferredDevice=''):
      """Connect to a preferred output MIDI device, or open a window to pick one.

      If the named device is not available, a window opens listing the output devices found.

      Args:
          preferredDevice (str, optional): The name of the output device to connect to. If omitted or unavailable, a selection window opens.
      """
      self.preferredDevice = preferredDevice

      availablePorts = mido.get_output_names()
      self.outputDevices = {}

      for port in availablePorts:
         self.outputDevices[port] = port

      if self.preferredDevice in self.outputDevices:
         self.openOutputDevice(self.preferredDevice)

      else:
         items = sorted(self.outputDevices.keys())

         if items:
            from gui import Display, DropDownList, Color

            self.display = Display("Select MIDI Output", 400, 125)
            self.display.drawLabel('Select a MIDI output device from the list', 45, 30)

            deviceDropdown = DropDownList(items, self.openOutputDevice)
            self.display.add(deviceDropdown, 40, 50)
            self.display.setColor( Color(255, 153, 153) )

            # Block until the user picks a device (callback on listener thread clears this)
            while self.waitingToSetup:
               time.sleep(0.01)

         else:
            print("MidiOut: No available MIDI output devices.")


   def openOutputDevice(self, selectedItem):
      """Open a named output MIDI device.

      This is the callback used by the device-selection window; you do not normally call it
      yourself.

      Args:
          selectedItem (str): The name of the output device to open.
      """
      global _activeMidiOutObjects

      try:
         print(f'MIDI output device set to "{selectedItem}".')
         deviceInfo = self.outputDevices[selectedItem]

         self.midiDeviceName = selectedItem
         self._port = mido.open_output(deviceInfo)
         self.waitingToSetup = False

         if self.display:
            self.display.close()

         _activeMidiOutObjects.append(self)

      except Exception as e:
         print(f"Error opening MIDI device: {e}")


##### Cleanup #########################################################################

def _stopActiveMidiObjects():
   """"""
   global _activeMidiInObjects, _activeMidiOutObjects

   for midiIn in _activeMidiInObjects.copy():
      try:
         midiIn.close()
      except Exception as e:
         print(f"Error closing MIDI input device: {e}")

   for midiOut in _activeMidiOutObjects.copy():
      try:
         midiOut.allNotesOff()
         midiOut.close()
      except Exception as e:
         print(f"Error closing MIDI output device: {e}")

   _activeMidiInObjects.clear()
   _activeMidiOutObjects.clear()

atexit.register(_stopActiveMidiObjects)

#######################################################################################
# Tests
#######################################################################################

if __name__ == "__main__":
   pass
