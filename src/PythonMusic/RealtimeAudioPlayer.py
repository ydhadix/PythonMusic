###############################################################################
# RealtimeAudioPlayer.py       Version 1.0     07-Nov-2025
# Trevor Ritchie, Taj Ballinger, and Bill Manaris
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
# 1.0   07-Nov-2025 (tr)   Initial implementation.
#
###############################################################################

import sounddevice as sd   # audio playback
import soundfile as sf     # audio file reading
import numpy as np         # array operations
import os                  # file path operations
import math                # log calculations in pitch/freq conversions

### Audio Data Cache ##########################################################
# Shared cache for audio file data to avoid loading the same file multiple times.
# This dramatically reduces memory usage when many AudioSample instances
# use the same large file.
# key: absolute file path (string)
# value: tuple of (audioData numpy array, sampleRate integer)
_audioDataCache = {}

### Conversion Functions ######################################################
def freqToNote(frequency):
   """
   Converts frequency to the closest MIDI note number with pitch bend value
   for finer control. A4 corresponds to the note number 69 (concert pitch
   is set to 440Hz by default). The default pitch bend range is 4 half tones,
   and ranges from -8191 to +8192 (0 means no pitch bend).
   """
   concertPitch = 440.0   # 440Hz
   bendRange = 4          # 4 semitones (2 below, 2 above)

   x = math.log(frequency / concertPitch, 2) * 12 + 69
   pitch = round(x)
   pitchBend = round((x - pitch) * 8192 / bendRange * 2)

   return int(pitch), int(pitchBend)


def noteToFreq(pitch):
   """
   Converts a MIDI pitch to the corresponding frequency. A4 corresponds
   to the note number 69 (concert pitch is set to 440Hz by default).
   """
   concertPitch = 440.0   # 440Hz
   frequency = concertPitch * 2 ** ( (pitch - 69) / 12.0 )

   return frequency


##### Realtime Audio Player ##################################################
class _RealtimeAudioPlayer:
   """
   Realtime audio engine for AudioSample polyphonic playback.
   Used by AudioSample in music.py for polyphonic audio playback.

   This class provides the low-level audio streaming infrastructure that powers
   AudioSample's polyphonic capabilities. AudioSample creates multiple instances
   of this class (one per voice) to enable complex musical compositions.

   The engine uses vectorized NumPy operations to process entire audio chunks at once
   rather than individual samples, achieving 3-6x speedup over traditional per-sample
   loops. This enables 16+ simultaneous voices with ~40% CPU usage compared to the
   unoptimized version which saturated at 4-8 voices.

   Optimization techniques:
   - Vectorized processing: process entire chunks with NumPy (10-100x faster)
   - Pre-allocated buffers: eliminate memory allocation in realtime callbacks
   - Time-stretch pitch shifting: vary playback speed with linear interpolation
   - Smooth transitions: fade envelopes prevent clicks when starting/stopping
   - Batch boundary detection: calculate loop points upfront, not per-sample

   Audio processing pipeline: Setup & Validation → Pitch Shifting → Dynamics
   Processing → Spatial Processing → Boundary Handling
   """

   def __init__(self, filepath, loop=False, actualPitch=69, chunkSize=1024):
      """
      Initialize realtime audio player - prepares audio engine for polyphonic playback.

      Sets up all components needed for high-performance audio playback including audio
      data loading, pitch/frequency control, panning, fades, and looping. Everything is
      pre-allocated to minimize realtime overhead since the audio callback must be
      extremely fast to avoid dropouts.

      filepath:    path to the audio file to load and play
      loop:        whether to loop the audio playback (default: False)
      actualPitch: MIDI pitch (0-127) representing the base frequency of the audio (default: 69 for A4)
      chunkSize:   size of audio chunks for realtime processing (default: 1024 frames)
      """
      #########################################################################
      # PHASE 1: AUDIO FILE LOADING & VALIDATION
      # load audio data into memory and validate format
      #########################################################################

      # convert to absolute path for consistent cache key (handles relative paths correctly)
      if not os.path.isabs(filepath):
         filepath = os.path.abspath(filepath)

      if not os.path.isfile(filepath):
         raise ValueError(f"File not found: {filepath}")

      self.filepath = filepath   # store the absolute file path for reference

      # check if audio data is already cached to avoid loading the same file multiple times
      # NOTE: sharing audio data across players saves significant memory when many voices use the same sample
      if filepath in _audioDataCache:
         # use cached audio data and sample rate (safe to share since audioData is read-only)
         self.audioData, self.sampleRate = _audioDataCache[filepath]
      else:
         # load the audio file using soundfile library
         try:
            self.audioData, self.sampleRate = sf.read(filepath, dtype='float32')
            # store in cache for future use (shared across all players using this file)
            _audioDataCache[filepath] = (self.audioData, self.sampleRate)
         except Exception as e:
            print(f"Error loading audio file with soundfile: {e}")
            raise

      # analyze audio format and store channel/frame information
      if self.audioData.ndim == 1:
         self.numChannels = 1   # mono audio
         self.numFrames = len(self.audioData)

      elif self.audioData.ndim == 2:
         self.numChannels = self.audioData.shape[1]   # sterio audio
         self.numFrames = self.audioData.shape[0]
         if self.numChannels > 2:
            raise ValueError(f"Unsupported number of channels: {self.numChannels}. Max 2 channels supported.")
      else:
         raise ValueError(f"Unexpected audio data dimensions: {self.audioData.ndim}")

      # check if the audio file contains any actual audio data
      if self.numFrames == 0:
         print(f"Warning: Audio file '{os.path.basename(self.filepath)}' contains zero audio frames and is unplayable.")

      #########################################################################
      # PHASE 2: PLAYBACK STATE INITIALIZATION
      # set up core playback control variables
      #########################################################################

      self.isPlaying = False
      self.playbackPosition = 0.0
      self.looping = loop
      self.rateFactor = 1.0
      self.volumeFactor = 1.0

      #########################################################################
      # PHASE 3: SPATIAL AUDIO (PANNING) INITIALIZATION
      # configure stereo positioning with smooth transitions
      # NOTE: smoothing prevents audible clicks when pan changes occur
      #########################################################################

      self.panTargetFactor = 0.0
      self.currentPanFactor = 0.0
      self.panInitialFactor = 0.0
      self.panSmoothingDurationMs = 100
      self.panSmoothingTotalFrames = max(1, int(self.sampleRate * (self.panSmoothingDurationMs / 1000.0)))
      self.panSmoothingFramesProcessed = self.panSmoothingTotalFrames

      #########################################################################
      # PHASE 4: PITCH/FREQUENCY CONTROL INITIALIZATION
      # establish base pitch for pitch-shifting calculations
      # NOTE: pitch shifting is implemented via time-stretch interpolation
      #########################################################################

      validPitchProvided = False
      if isinstance(actualPitch, (int, float)):
         tempPitch = float(actualPitch)

         if 0 <= tempPitch <= 127:   # validate MIDI pitch range
            self.basePitch = tempPitch
            self.baseFrequency = noteToFreq(self.basePitch)   # convert MIDI pitch to frequency
            validPitchProvided = True

      if not validPitchProvided:
         # handle invalid pitch values by defaulting to A4 (440Hz)
         print(f"Warning: Invalid or out-of-range actualPitch ({actualPitch}) provided for '{os.path.basename(self.filepath)}'.\
                Expected MIDI pitch (int/float) 0-127. Defaulting to A4 (69 / 440Hz).")
         self.basePitch = 69.0   # default MIDI A4
         self.baseFrequency = noteToFreq(self.basePitch)   # default 440 Hz

      #########################################################################
      # PHASE 5: FADE ENVELOPE INITIALIZATION
      # configure smooth fades to prevent clicks/pops
      # NOTE: fades are essential for professional audio quality
      #########################################################################

      self.fadeInDurationMs = 20       # fade-in duration in milliseconds
      self.fadeInFramesProcessed = 0   # frames processed during current fade-in
      self.isApplyingFadeIn = False    # whether fade-in is currently active
      self.fadeInTotalFrames = max(1, int(self.sampleRate * (self.fadeInDurationMs / 1000.0)))

      self.fadeOutDurationMs = 20           # fade-out duration in milliseconds
      self.fadeOutFramesProcessed = 0       # frames processed during current fade-out
      self.isApplyingFadeOut = False        # whether fade-out is currently active
      self.isFadingOutToStop = False        # whether fade-out is leading to a stop
      self.isFadingOutToSeek = False        # whether fade-out is leading to a seek operation
      self.seekTargetFrameAfterFade = 0.0   # target frame position after seek fade completes
      self.fadeOutTotalFrames = max(1, int(self.sampleRate * (self.fadeOutDurationMs / 1000.0)))

      #########################################################################
      # PHASE 6: AUDIO STREAM & BUFFER INITIALIZATION
      # pre-allocate audio stream and processing buffers
      # NOTE: pre-allocation is key optimization - eliminates runtime allocations
      #########################################################################

      self.sdStream = None         # sounddevice OutputStream for playback
      self.chunkSize = chunkSize   # audio block size to process per callback

      # pre-allocate buffers for vectorized processing (major performance optimization)
      # NOTE: reusing these buffers across callbacks eliminates memory allocation overhead
      maxChunkSize = chunkSize * 2
      self.chunkBuffer = np.zeros((maxChunkSize, 2), dtype=np.float32)
      self.processedSampleBuffer = np.zeros((maxChunkSize, 2), dtype=np.float32)
      self.readPositions = np.zeros(maxChunkSize, dtype=np.float64)
      self.fadeEnvelope = np.ones(maxChunkSize, dtype=np.float32)

      #########################################################################
      # PHASE 7: LOOP & PLAYBACK CONTROL INITIALIZATION
      # set up loop regions and playback duration tracking
      #########################################################################

      self.playbackEndedNaturally = False    # whether playback ended naturally (not stopped)
      self.playDurationSourceFrames = -1.0   # play duration in source frames (-1 = play to end)
      self.targetEndSourceFrame = -1.0       # target end frame for play duration (-1 = play to end)
      self.loopRegionStartFrame = 0.0        # start frame of loop region
      self.loopRegionEndFrame = -1.0         # end frame of loop region (-1 means to end of file)
      self.loopCountTarget = -1              # target loop count (-1 = infinite, 0 = no loop, 1+ = specific count)
      self.loopsPerformed = 0                # number of loops completed so far
      self.isClosed = False                  # track whether close() has been called

      if self.looping and self.loopCountTarget == -1:
         pass   # infinite looping
      elif not self.looping:
         self.loopCountTarget = 0   # play once

      #########################################################################
      # PHASE 8: AUDIO STREAM CREATION
      # create (but don't start) the audio stream for immediate playback readiness
      # NOTE: stream is created now but started later in play() for maximum efficiency
      #########################################################################

      self.createStream()

   ### Playback Control Methods ###############################################
   def play(self, startAtBeginning=True, loop=None, playDurationSourceFrames=-1.0,
            loopRegionStartFrame=0.0, loopRegionEndFrame=-1.0, loopCountTarget=None,
            initialLoopsPerformed=0):

      # does audio file contain zero frames?
      if self.numFrames == 0:
         # if so, do not attempt to play
         print(f"Cannot play '{os.path.basename(self.filepath)}' as it contains zero audio frames.")
         self.isPlaying = False   # ensure state consistency
         return   # do not proceed to start a stream
         # TODO: rewrite to avoid early return

      # is a fade-out to stop currently in progress?
      if self.isFadingOutToStop:
         # if so, reset fade-out state before playing
         self.isApplyingFadeOut = False
         self.isFadingOutToStop = False
         self.fadeOutFramesProcessed = 0

      # determine definitive looping state and count from parameters
      if loop is not None:
         self.looping = bool(loop)

      elif loopCountTarget is not None: # loop is None, derive from loopCountTarget
         self.looping = True if loopCountTarget != 0 else False

      # Now, if both loop and loopCountTarget are None, self.looping is unchanged (relevant if stream is already playing)
      # or takes its initial value from __init__ if stream is being started for the first time.

      # determine how many times to loop (or not) based on input and current looping state
      if loopCountTarget is not None:
         self.loopCountTarget = loopCountTarget   # use the provided loop count

      elif self.looping:   # no explicit loop count, but looping is enabled
         self.loopCountTarget = -1   # default to infinite looping

      else:   # not looping and no loop count specified
         self.loopCountTarget = 0   # play once by default

      # ensure consistency: if loopCountTarget implies a certain looping state, it can refine self.looping
      if self.loopCountTarget == 0: # explicitly play once for this segment
         self.looping = False

      elif self.loopCountTarget == -1 or self.loopCountTarget > 0: # infinite or positive count implies looping
         self.looping = True

      # store parameters
      self.playDurationSourceFrames = playDurationSourceFrames   # used if not self.looping
      self.loopRegionStartFrame = max(0.0, float(loopRegionStartFrame))
      self.loopRegionEndFrame = float(loopRegionEndFrame) if loopRegionEndFrame is not None else -1.0

      # adjust the loop region end frame so it does not exceed the end of the audio file
      if self.loopRegionEndFrame > 0:
         self.loopRegionEndFrame = min(self.loopRegionEndFrame, float(self.numFrames))

      # ensure the loop region is valid: if the start frame is after or equal to the end frame, reset to default (full file)
      if self.numFrames > 0 and self.loopRegionEndFrame > 0 and self.loopRegionStartFrame >= self.loopRegionEndFrame:
         self.loopRegionStartFrame = 0.0
         self.loopRegionEndFrame = -1.0   # default to looping the entire file

      # determine the stopping point for playback based on looping and duration settings
      if self.looping:
         # when looping, ignore playDurationSourceFrames and play until loop count is reached or forever
         self.targetEndSourceFrame = -1.0

      elif self.playDurationSourceFrames >= 0:
         # when not looping but a specific play duration is requested, calculate the end frame for playback
         currentStartForCalc = self.playbackPosition if not startAtBeginning else self.loopRegionStartFrame
         self.targetEndSourceFrame = currentStartForCalc + self.playDurationSourceFrames
         # self.loopCountTarget is already 0 if not looping

      else:
         # when not looping and no duration is specified, play until the natural end of the file
         self.targetEndSourceFrame = -1.0
         # self.loopCountTarget is already 0

      # handle playback position and loops performed count based on startAtBeginning and initialLoopsPerformed
      if startAtBeginning:
         self.playbackPosition = self.loopRegionStartFrame # start at the beginning of the loop region (or 0 if not specified)
         self.loopsPerformed = initialLoopsPerformed # typically 0 for a fresh start from beginning

      else: # resuming (startAtBeginning=False)
         # playbackPosition is where it was left off by pause or setCurrentTime
         self.loopsPerformed = initialLoopsPerformed   # restore from argument

      self.playbackEndedNaturally = False   # reset this flag as we are starting/resuming a play action

      # if already playing, these settings will take effect, but stream isn't restarted

      # if not playing, start the stream.
      if not self.isPlaying:

         if self.playbackPosition >= self.numFrames and not self.looping:
            self.playbackPosition = 0.0   # or self._findNextZeroCrossing(0.0)

         self.playbackEndedNaturally = False   # playback did not reach the end

         try:
            # always start with a fade-in when initiating play from a stopped state or from a fade-out-to-stop state
            self.isApplyingFadeIn = True
            self.fadeInFramesProcessed = 0

            # Use the pre-allocated stream - start it if it's not already running
            if self.sdStream and not self.sdStream.closed:
               if self.sdStream.stopped:
                  # Stream exists but is stopped, so start it
                  self.sdStream.start()

               self.isPlaying = True
               self.playbackEndedNaturally = False
            else:
               # stream was somehow lost - recreate it
               self.isClosed = False   # reset closed flag to allow recreation
               self.createStream()
               if self.sdStream is not None:
                  self.sdStream.start()   # start the newly created stream
                  self.isPlaying = True
                  self.playbackEndedNaturally = False

         except Exception as e:   # stream recreation failed
            print(f"Error with audio stream: {e}")
            self.isPlaying = False
            return   # exit since stream failed

         if startAtBeginning and self.isPlaying:   # check isPlaying again in case it was set by new stream
            self.isApplyingFadeIn = True
            self.fadeInFramesProcessed = 0

   def stop(self, immediate=False):
      """
      Stops audio playback with optional immediate termination.

      This method provides two stopping modes: immediate (instant stop) and gradual
      (fade-out stop). The method handles cleanup of audio streams, resets playback
      state variables, and manages fade transitions appropriately.
      """
      # handle case where already stopped (but may have pending fade-out)
      if not self.isPlaying and not self.isApplyingFadeOut:

         # Ensure stream is stopped when not playing
         if self.sdStream and not self.sdStream.stopped:
            try:
               self.sdStream.stop()
            except Exception:
               # ignore errors during cleanup
               pass

         # reset all playback state variables
         self.isPlaying = False   # confirm stopped state
         self.targetEndSourceFrame = -1.0   # reset end frame target
         self.playDurationSourceFrames = -1.0   # reset duration tracking

         # reset loop attributes on stop
         self.loopRegionStartFrame = 0.0   # reset loop start to beginning
         self.loopRegionEndFrame = -1.0   # reset loop end to no loop
         self.loopCountTarget = -1 if self.looping else 0   # reset to constructor state
         self.loopsPerformed = 0   # reset loop counter
         return   # done, since already stopped

      # handle immediate stop (skip fade-out for instant termination)
      if immediate:
         # immediately signal all playback logic to stop
         self.isPlaying = False   # signal callback to stop producing audio
         self.isApplyingFadeIn = False   # cancel any ongoing fade-in
         self.isApplyingFadeOut = False   # cancel any ongoing fade-out (e.g. from pause)
         self.isFadingOutToStop = False   # ensure fade-out-to-stop is reset

         # Stop the stream when stopping immediately
         if self.sdStream and not self.sdStream.stopped:
            try:
               self.sdStream.stop()
            except Exception:
               # ignore errors during cleanup
               pass

         # reset all playback state variables for immediate stop
         self.targetEndSourceFrame = -1.0       # reset end frame target
         self.playDurationSourceFrames = -1.0   # reset duration tracking
         self.loopRegionStartFrame = 0.0        # reset loop start to beginning
         self.loopRegionEndFrame = -1.0         # reset loop end to no loop
         self.loopCountTarget = -1 if self.looping else 0   # reset to constructor state
         self.loopsPerformed = 0   # reset loop counter

      else:   # gradual stop (fade out)

         # only start a fade-out if actually playing or was about to start
         if self.isPlaying or self.isApplyingFadeIn:
            self.isApplyingFadeIn = False     # stop any fade-in
            self.isApplyingFadeOut = True     # start fade-out process
            self.isFadingOutToStop = True     # mark that this fade-out is intended to stop playback
            self.fadeOutFramesProcessed = 0   # reset fade-out progress counter
            # isPlaying remains true until fade-out completes in the callback

      # now, the sounddevice stream is stopped

   ### Playback State Methods #################################################
   def getCurrentTime(self):
      # calculate current time based on position and sample rate
      currentTime = self.playbackPosition / self.sampleRate
      return currentTime   # return current time

   def setCurrentTime(self, timeSeconds):
      # check that timeSeconds is a valid non-negative number. if not, default to 0.0
      if not isinstance(timeSeconds, (int, float)) or timeSeconds < 0:
         timeSeconds = 0.0

      # convert the requested time in seconds to a floating-point frame index
      originalTargetFrameFloat = timeSeconds * self.sampleRate

      # basic ZC adjustment for now, will be enhanced with fade-seek-fade
      actualTargetFrame = self.findNextZeroCrossing(originalTargetFrameFloat)

      # if playing and conditions met for smooth seek
      if actualTargetFrame >= self.numFrames and not self.looping:
         # set playback position to the requested frame, or to the end if beyond available frames
         self.playbackPosition = float(self.numFrames -1)
         self.playbackEndedNaturally = True

      else:
         self.playbackPosition = actualTargetFrame   # set playback position to the next zero crossing
         self.playbackEndedNaturally = False   # reset natural end flag if jumping

   def getLoopsPerformed(self):
      return self.loopsPerformed  # number of loops completed

   def getFrameRate(self):
      return self.sampleRate   # sample rate of the audio

   ### Audio Parameter Methods ################################################
   def setPitch(self, midiPitch):
      # set the playback pitch by converting midiPitch (0-127) to frequency and updating rate factor
      if (isinstance(midiPitch, (int, float)) and 0 <= midiPitch <= 127):
         targetFrequencyHz = noteToFreq(float(midiPitch))   # convert midi pitch to frequency
         self.setFrequency(targetFrequencyHz)               # set playback frequency accordingly

   def getPitch(self):
      currentFreq = self.getFrequency()        # get freq
      currentPitch = freqToNote(currentFreq)   # convert to pitch
      return currentPitch   # return current pitch

   def getBasePitch(self):
      return self.basePitch   # original pitch of the sample

   def setFrequency(self, targetFrequencyHz):
      if isinstance(targetFrequencyHz, (int, float)) and self.baseFrequency > 0:

         if targetFrequencyHz > 0:   # frequency is valid
            newRateFactor = targetFrequencyHz / self.baseFrequency
            self.setRateFactor(newRateFactor)

         else:   # target frequency too small
            self.setRateFactor(0.00001)   # avoid zero or negative, effectively silent/pause

   def getFrequency(self):
      # calculate current frequency based on base and rate
      currentFreq = self.baseFrequency * self.rateFactor
      return currentFreq   # return current frequency

   def getBaseFrequency(self):
      return self.baseFrequency   # original frequency of the sample

   def setVolumeFactor(self, factor):
      if isinstance(factor, (int, float)):
         # valid factor, so set volume
         self.volumeFactor = max(0.0, min(1.0, float(factor)))
         # print(f"Set to {self.volumeFactor:.3f}")

      else:
         # factor is invalid type, so default to full volume
         self.volumeFactor = 1.0

   def getVolumeFactor(self):
      return self.volumeFactor   # return volume factor

   def setPanFactor(self, panFactor):
      # clamp panFactor to a float in [-1.0, 1.0]; if invalid, default to center (0.0)
      if not isinstance(panFactor, (int, float)):
         clampedPanFactor = 0.0   # not a number, so use center

      else:
         clampedPanFactor = max(-1.0, min(1.0, float(panFactor)))   # clamp to valid range

      # if the new pan target is different enough from the current target, start smoothing ramp
      if abs(self.panTargetFactor - clampedPanFactor) > 0.001:   # significant change
         self.panTargetFactor = clampedPanFactor   # set new pan target
         self.panInitialFactor = self.currentPanFactor   # remember current pan as ramp start
         self.panSmoothingFramesProcessed = 0   # reset smoothing progress

   def getPanFactor(self):
      return self.panTargetFactor   # return pan factor

   def setRateFactor(self, factor):
      # check if the provided factor is a number (int or float)
      if isinstance(factor, (int, float)):

         # if factor is zero or negative, set to a very small positive value to effectively pause playback
         if factor <= 0:
            self.rateFactor = 0.00001   # avoid zero or negative, effectively silent/pause

         else:
            # otherwise, set the rate factor to the given value (as float)
            self.rateFactor = float(factor)
         # print(f"Set to {self.rateFactor:.4f}")

      else:
         # if input is not a number, default to 1x speed
         self.rateFactor = 1.0

   def getRateFactor(self):
      return self.rateFactor   # return rate factor

   ### Internal Audio Engine Methods #########################################
   def createStream(self):
      """
      Creates and starts the audio stream. This method is called during initialization
      to pre-allocate the stream for maximum efficiency.
      """
      try:
         # create the sounddevice output stream for playback
         self.sdStream = sd.OutputStream(
            samplerate=self.sampleRate,
            blocksize=self.chunkSize,
            channels=self.numChannels,
            callback=self.audioCallback
         )

         # Don't start the stream here - it will be started in play() method
         # self.sdStream.start()  # Stream will be started when needed

      except Exception as e:
         print(f"Error creating audio stream: {e}")
         self.sdStream = None
         raise

   def findNextZeroCrossing(self, startFrameFloat, searchWindowFrames=256):
      """
      Find the nearest zero-crossing point in the audio waveform.

      Zero-crossings are points where the audio signal crosses the zero amplitude line.
      Starting/stopping playback at zero-crossings prevents audible clicks and pops that
      occur when abruptly cutting audio at non-zero amplitudes. This is especially important
      for seek operations and loop boundaries.

      Uses vectorized NumPy operations to efficiently search a window of samples rather than
      checking each sample individually.
      """
      # convert floating-point frame position to integer and clamp to valid range
      startFrame = int(np.floor(startFrameFloat))
      startFrame = max(0, min(startFrame, self.numFrames - 1))

      # limit search window to prevent going beyond audio data boundaries
      # NOTE: 256 frames is ~5ms at 48kHz - short enough to be inaudible
      endSearchFrame = min(self.numFrames - 1, startFrame + searchWindowFrames)

      if startFrame >= self.numFrames - 1:
         return float(min(startFrame, self.numFrames - 1))

      # extract audio segment for search (use left channel for stereo)
      if self.numChannels == 1:
         segment = self.audioData[startFrame:endSearchFrame]
      else:
         segment = self.audioData[startFrame:endSearchFrame, 0]

      # check if we have enough samples to search
      if len(segment) < 2:
         return float(startFrame)

      # vectorized zero-crossing detection - much faster than sample-by-sample loop
      # first, look for samples that are exactly zero (rare but ideal)
      zeroIndices = np.where(segment == 0.0)[0]
      if len(zeroIndices) > 0:
         return float(startFrame + zeroIndices[0])

      # find sign changes (positive to negative or vice versa) which indicate zero-crossings
      # NOTE: np.diff finds differences between consecutive samples, sign changes indicate crossings
      signChanges = np.diff(np.sign(segment))
      crossingIndices = np.where(signChanges != 0)[0]

      if len(crossingIndices) > 0:
         # return frame just after the crossing
         return float(startFrame + crossingIndices[0] + 1)

      # no crossing found in search window - return original position
      # NOTE: this is okay, the fade envelope will still minimize clicks
      return float(startFrame)

   def audioCallback(self, outdata, frames, time, status):
      """
      Real-time audio processing callback.

      Called repeatedly by sounddevice to fill the audio output buffer. Processes
      entire chunks using vectorized NumPy operations for maximum performance,
      enabling high polyphony without CPU bottlenecks.

      Five-phase processing pipeline:
         1. Setup & Validation
         2. Pitch Shifting (via time-stretch interpolation)
         3. Dynamics Processing (volume, fades)
         4. Spatial Processing (panning)
         5. Boundary Handling (looping, playback completion)
      """
      #########################################################################
      # PHASE 1: SETUP & VALIDATION
      # validate audio state and prepare for processing
      #########################################################################

      # handle edge cases that require silence
      if self.numFrames == 0:
         outdata.fill(0)
         if self.isPlaying:
            self.isPlaying = False
         raise sd.CallbackStop

      # early return for silence conditions
      if not self.isPlaying or self.rateFactor <= 0.000001:
         outdata.fill(0)
         if self.isApplyingFadeOut and self.isFadingOutToStop and self.rateFactor <= 0.000001:
            self.isPlaying = False
            self.isApplyingFadeOut = False
            self.isFadingOutToStop = False
         return

      # cache attributes as local variables
      # NOTE: reduces attribute lookup overhead in hot path (significant performance gain)
      numOutputChannels = outdata.shape[1]
      numSourceChannels = self.numChannels
      rateFactor = self.rateFactor
      volumeFactor = self.volumeFactor
      currentPan = self.currentPanFactor
      looping = self.looping
      numAudioFrames = self.numFrames

      # determine where playback should end for this segment
      # NOTE: supports three modes: natural EOF, loop region end, or play(size) duration
      # effectiveSegmentEndFrame is the exclusive end (first frame NOT to play)
      effectiveSegmentEndFrame = float(numAudioFrames)
      if looping and self.loopRegionEndFrame > 0:
         effectiveSegmentEndFrame = self.loopRegionEndFrame
      elif not looping and self.targetEndSourceFrame > 0:
         effectiveSegmentEndFrame = self.targetEndSourceFrame

      # calculate safe processing range before hitting boundaries
      # NOTE: batch boundary detection avoids per-sample checks (major optimization)
      framesToProcess = frames
      willHitBoundary = False

      if effectiveSegmentEndFrame > 0:
         framesToEndpoint = (effectiveSegmentEndFrame - self.playbackPosition) / rateFactor
         if 0 <= framesToEndpoint < frames:
            willHitBoundary = True
            # ceil gives the number of frames that stay strictly within the endpoint
            framesToProcess = min(frames, int(np.ceil(framesToEndpoint)))

      ###########################################################################
      # PHASE 2: PITCH SHIFTING VIA TIME-STRETCH INTERPOLATION
      # generate audio at requested pitch by resampling source audio
      # NOTE: this is where pitch/frequency changes are actually applied
      ###########################################################################

      # generate array of source read positions for entire chunk
      # NOTE: vectorized - processes all frames at once instead of per-sample loop
      readPositionsArray = self.playbackPosition + np.arange(framesToProcess, dtype=np.float64) * rateFactor
      readPositionsArray = np.clip(readPositionsArray, 0.0, numAudioFrames - 1.0)

      # calculate interpolation parameters for smooth resampling
      # NOTE: integer positions (samples to read) and fractions (for interpolation)
      readPosInt1 = np.floor(readPositionsArray).astype(np.int32)
      readPosInt2 = np.minimum(readPosInt1 + 1, numAudioFrames - 1)
      fractions = readPositionsArray - readPosInt1

      # perform vectorized linear interpolation
      # NOTE: handles mono/stereo automatically, interpolates entire chunk at once
      if numSourceChannels == 1:   # mono source
         samples1 = self.audioData[readPosInt1]
         samples2 = self.audioData[readPosInt2]
         interpolatedSamples = samples1 + (samples2 - samples1) * fractions
         interpolatedSamples = interpolatedSamples.reshape(-1, 1)   # shape: (framesToProcess, 1)

      else:   # stereo source
         samples1 = self.audioData[readPosInt1, :]
         samples2 = self.audioData[readPosInt2, :]
         fractions2D = fractions.reshape(-1, 1)
         interpolatedSamples = samples1 + (samples2 - samples1) * fractions2D   # shape: (framesToProcess, 2)

      #########################################################################
      # PHASE 3: DYNAMICS PROCESSING
      # apply volume control and smooth fades to prevent clicks/pops
      #########################################################################

      # apply volume scaling
      processedSamples = interpolatedSamples * volumeFactor

      # generate fade envelope for smooth transitions
      # NOTE: fades prevent audible clicks when starting/stopping audio
      fadeEnv = np.ones(framesToProcess, dtype=np.float32)

      # apply fade-in envelope if transitioning from silence
      if self.isApplyingFadeIn:
         remainingFadeInFrames = self.fadeInTotalFrames - self.fadeInFramesProcessed

         if remainingFadeInFrames > 0:
            fadeInLength = min(remainingFadeInFrames, framesToProcess)
            startValue = self.fadeInFramesProcessed / self.fadeInTotalFrames
            endValue = (self.fadeInFramesProcessed + fadeInLength) / self.fadeInTotalFrames
            fadeEnv[:fadeInLength] *= np.linspace(startValue, endValue, fadeInLength, dtype=np.float32)
            self.fadeInFramesProcessed += fadeInLength

            if self.fadeInFramesProcessed >= self.fadeInTotalFrames:
               self.isApplyingFadeIn = False

      # apply fade-out envelope if transitioning to silence
      if self.isApplyingFadeOut:
         remainingFadeOutFrames = self.fadeOutTotalFrames - self.fadeOutFramesProcessed
         if remainingFadeOutFrames > 0:
            fadeOutLength = min(remainingFadeOutFrames, framesToProcess)
            startValue = 1.0 - (self.fadeOutFramesProcessed / self.fadeOutTotalFrames)
            endValue = 1.0 - ((self.fadeOutFramesProcessed + fadeOutLength) / self.fadeOutTotalFrames)
            fadeEnv[:fadeOutLength] *= np.linspace(startValue, endValue, fadeOutLength, dtype=np.float32)
            self.fadeOutFramesProcessed += fadeOutLength

            if self.fadeOutFramesProcessed >= self.fadeOutTotalFrames:
               self.isApplyingFadeOut = False

               if self.isFadingOutToStop:
                  self.isPlaying = False
                  self.isFadingOutToStop = False
                  self.targetEndSourceFrame = -1.0
                  self.playDurationSourceFrames = -1.0
                  # fill remainder with silence
                  fadeEnv[fadeOutLength:] = 0.0

         else:
            fadeEnv[:] = 0.0

      # apply combined fade envelope to audio
      processedSamples = processedSamples * fadeEnv.reshape(-1, 1)

      #########################################################################
      # PHASE 4: SPATIAL PROCESSING
      # position audio in stereo field using psychoacoustic panning
      #########################################################################

      # apply constant-power panning for stereo output
      # NOTE: constant-power law maintains perceived loudness across pan positions
      if numOutputChannels == 2:   # stereo output
         panAngleRad = (currentPan + 1.0) * np.pi / 4.0
         leftGain = np.cos(panAngleRad)
         rightGain = np.sin(panAngleRad)

         if numSourceChannels == 1:   # mono to stereo
            outdata[:framesToProcess, 0] = processedSamples[:, 0] * leftGain
            outdata[:framesToProcess, 1] = processedSamples[:, 0] * rightGain
         else:   # stereo to stereo
            outdata[:framesToProcess, 0] = processedSamples[:, 0] * leftGain
            outdata[:framesToProcess, 1] = processedSamples[:, 1] * rightGain

      # handle mono output (no panning needed, mix stereo to mono if needed)
      else:   # mono output
         if numSourceChannels == 1:   # mono to mono
            outdata[:framesToProcess, 0] = processedSamples[:, 0]
         else:   # stereo to mono (mixdown)
            outdata[:framesToProcess, 0] = (processedSamples[:, 0] + processedSamples[:, 1]) * 0.5

      #########################################################################
      # PHASE 5: BOUNDARY HANDLING & LOOP MANAGEMENT
      # handle end-of-audio, looping, and playback completion
      #########################################################################

      # update playback position for next callback
      self.playbackPosition += framesToProcess * rateFactor

      # handle segment boundaries (loop wrap or playback end)
      if willHitBoundary or self.playbackPosition >= effectiveSegmentEndFrame:
         if looping:
            self.loopsPerformed += 1
            if self.loopCountTarget != -1 and self.loopsPerformed >= self.loopCountTarget:
               # loop count reached - stop playback
               self.isPlaying = False
               self.loopsPerformed = 0
               # fill remainder with silence
               if framesToProcess < frames:
                  outdata[framesToProcess:, :] = 0.0
            else:
               # continue looping - wrap back to loop start
               self.playbackPosition = self.loopRegionStartFrame
               if framesToProcess < frames:
                  remainingFrames = frames - framesToProcess
                  tempOutdata = outdata[framesToProcess:, :]
                  self.audioCallback(tempOutdata, remainingFrames, time, status)
         else:
            # non-looping playback reached end
            self.isPlaying = False
            if self.playbackPosition >= numAudioFrames - 1:
               self.playbackEndedNaturally = True
            self.targetEndSourceFrame = -1.0
            self.playDurationSourceFrames = -1.0
            # fill remainder with silence
            if framesToProcess < frames:
               outdata[framesToProcess:, :] = 0.0

      # safety - fill any unfilled portion with silence
      # skip when willHitBoundary is True: boundary handling already filled remainder (via recursion or explicit zero-fill)
      if framesToProcess < frames and self.isPlaying and not willHitBoundary:
         outdata[framesToProcess:, :] = 0.0

      # update pan smoothing (prevents clicks from abrupt pan changes)
      # NOTE: processed at block level for efficiency
      if self.panSmoothingFramesProcessed < self.panSmoothingTotalFrames:
         self.panSmoothingFramesProcessed += frames

         if self.panSmoothingFramesProcessed >= self.panSmoothingTotalFrames:
            self.currentPanFactor = self.panTargetFactor
            self.panSmoothingFramesProcessed = self.panSmoothingTotalFrames
         else:
            t = self.panSmoothingFramesProcessed / self.panSmoothingTotalFrames
            self.currentPanFactor = self.panInitialFactor + (self.panTargetFactor - self.panInitialFactor) * t

      else:
         self.currentPanFactor = self.panTargetFactor

      # safety clipping to prevent distortion
      # NOTE: ensures all samples are within valid range for audio hardware
      np.clip(outdata, -1.0, 1.0, out=outdata)


   ### Cleanup Methods #######################################################
   def __del__(self):
      """
      Destructor - ensures resources are released when object is garbage collected.

      Safely calls close() and suppresses all exceptions since we can't handle them
      during garbage collection. This is critical because __del__ may be called during
      interpreter shutdown when other objects/modules may already be cleaned up.
      """
      try:
         self.close()
      except Exception:
         pass   # never let exceptions escape from __del__

   def close(self):
      """
      Release all audio resources and stop playback.

      Safe to call multiple times - subsequent calls are ignored. After calling close(),
      the player can still be used again via play() which will recreate the stream.

      This method stops any active playback, cancels pending fades, and releases the
      audio stream resources. It's automatically called during garbage collection but
      can also be called explicitly for immediate cleanup.
      """
      if not self.isClosed:   # prevent double cleanup
         self.isClosed = True     # mark as closed before attempting cleanup
         self.isPlaying = False   # ensure any playback logic stops

         # cancel any pending fades that might try to operate on a closing stream
         self.isApplyingFadeIn = False
         self.isApplyingFadeOut = False
         self.isFadingOutToStop = False

         if self.sdStream:
            try:
               # check if stream is active before trying to stop
               if not self.sdStream.stopped:
                  self.sdStream.stop()   # stop stream activity

               # re-check because .stop() could have been called
               if not self.sdStream.closed:
                  self.sdStream.close()   # release resources

            except Exception as e:
               # catch all exceptions for robust cleanup
               if isinstance(e, sd.PortAudioError):
                  # if PortAudio is already uninitialized (e.g. during atexit), suppress error
                  paNotInitialized = getattr(sd, 'PaErrorCode', None)
                  if paNotInitialized and len(e.args) > 1 and e.args[1] == paNotInitialized.paNotInitialized:
                     pass   # suppress error if PortAudio is already down
                  else:
                     print(f"PortAudioError during stream stop/close: {e}")
               else:
                  print(f"Error during stream cleanup: {e}")
            finally:
               self.sdStream = None
