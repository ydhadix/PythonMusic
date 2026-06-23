"""
PianoRoll is a piano roll representation of a JythonMusic/jMusic Score.
This representation assignes voices to notes, using a heuristic algorithm
that minimizes voice crossings and large jumps within a voice.

Reference::  See Chew and Wu, "Separating Voices in Polyphonic Music:
A Contig Mapping Approach" (see ecxw-cmmr2004.pdf in the source file directory,
or http://www-rcf.usc.edu/~echew/papers/CMMR2004/ecxw-cmmr2004.pdf
"""

import math
from music import Score, Part, Phrase, Note, PIANO, REST
from .ExtendedNote import ExtendedNote
from .Contig import Contig


class PianoRoll:
   """
   PianoRoll is a piano roll representation of a JythonMusic/jMusic Score.
   This representation assignes voices to notes, using a heuristic algorithm
   that minimizes voice crossings and large jumps within a voice.


   Reference::  See Chew and Wu, "Separating Voices in Polyphonic Music:
   A Contig Mapping Approach" (see ecxw-cmmr2004.pdf in the source file directory,
   or http://www-rcf.usc.edu/~echew/papers/CMMR2004/ecxw-cmmr2004.pdf


   Notes:
     Q: How does jMusic represent time?
     A: JMusic represents time (e.g., start time of a Phrase, rhythm value of a note)
        as a real number (independent of the time-signature).  For example,
        4.0 means a whole note, 2.0 a half, 1.0 a quarter, 0.5 an eighth, etc.

     Q: What is a quantum?
     A: A piano roll consists of time slices.  The width (temporal duration) of each slice
        is a quantum. When filling the piano roll, a note longer than the quantum fills several quantums.
        Remainders that are less than a quantum are dropped, as are notes less than one quantum in duration.
        This, in essense, quantizes the note's start time and duration.
        The smaller the quantum, the more detailed the piano roll representation will be and the smaller
        the notes, rests, etc. that can be represented in the piano roll.


   author Brian Muller, Tim Hirzel, Bill Manaris, Hector Mojica, Patrick Roos
   version 20-03-06
   """

   def __init__(self, score, quantum=0.25, maxVoiceJump=7):
      """
      Create a PianoRoll to represent the Score with desired quantum and
      maximum voice jump.

      param score: the Score to be represented as a PianoRoll.
      param quantum: the width (duration) of each timeslice in the pianoroll representation.
      param maxVoiceJump: the maximum jump allowed between consecutive notes in each voice.

      Note: The shorter the quantum, the more detailed the pianoroll representation will be.
      Longer quantums will result in less detail in the representation of the Score,
      because remainders (left when a note is longer than a quantum)and single notes that are less than the quantum are dropped.
      A quantum length of the shortest note in the score is not small enough to represent the score lossless and perfectly unskewed in the pianoroll.
      This is due to possible rests that are shorter, and the related fact that start times of notes usually will not be in synch
      with the beginning of timeslices, resulting in shifting of notes in the pianoroll representation and thus possibly remainders
      of notes which are shorter than a quantum and thus dropped.
      """
      self.numberOfVoices = 0   # the scores maximum number of voices at any point in the pianoroll representation

      # set to true when testing to get output
      self.TEST_OUTPUT = False
      # self.TEST_OUTPUT = True

      # retain these so a score can be recreated in "getScore"
      self.numerator = score.getNumerator()      # the score's time-signature numerator
      self.denominator = score.getDenominator()  # the score's time-signature denominator
      self.tempo = score.getTempo()              # the score's tempo

      # set time slice duration
      self.quantum = quantum

      # maximum pitch interval (in semitones) allowed between two
      # consecutive notes in a voice
      self.maxVoiceJump = maxVoiceJump   # 7 is a P5, 5 is P4, 4 is M3, 3 is m3...

      if self.TEST_OUTPUT:
         print("Score's original tempo: " + str(score.getTempo()))

      # contains all notes in the Score (ordered by start time)
      # NOTE: 0th element is left empy, due to how continutations are represented (see pianoRoll[][])
      # create the note array with the given score
      self.noteArray = self._createArray(score)

      # The piano roll representation.  First dimension corresponds to time (or time slice),
      # equal to a quantum.  Each time slice (second dimension) identifies which
      # notes are currently sounding (by storing indeces into the 'noteArray').
      # A negative index indicates a note continuation (i.e., note started sounding
      # in an earlier time slice.  Each time slice is ordered by voice of the
      # note sounding (i.e., NOT by index value, but by the voice of the note
      # being pointed by the index).
      # populate the piano roll with the array note indices
      self.pianoRoll = self._populatePianoRoll(self.noteArray, self.quantum, score.getEndTime())

      # assign a voice to each note
      self._assignRollVoices(self.pianoRoll)

   def _createArray(self, score):
      """
      Returns an array of extended notes representing the score (first note is at index 1, 0 is empty,
      due to how continuations are represented).

      param Score score: the initial score to be used to create the new PianoRoll object.
      return list[ExtendedNote]: an extended note array - assigned to class instance variable, sorted first by start time, and then by pitch (lowest to highest)
      """
      allNoteArray = []   # holds all notes in the score

      # Build the allNoteVector by filling it with ExtendedNotes,
      # which are Notes objects extended to include their start time.
      parts = score.getPartList()

      # This variable is used to keep track of what the "time" is
      # as the score is traversed (in jMusic units, e.g., 1 = quarter note)
      currentTime = 0.0

      # Holds all notes in the allNoteVector, so that they be sorted.
      # The first element (index 0) is not used, since the piano roll uses
      # a negative index to signify continuation of a note (0 cannot be negated).

      # In this next succession of loops we will be traversing the score
      # drilling down to smaller and smaller elements (part -> phrase ->  note)
      # until we can count each note.  A currentTime variable will be updated at the lower
      # level to keep track of the "current" time as the loops progress - this time
      # and each note will be combined to form an extended note and then added to the
      # note array.
      for part in parts:
         phrases = part.getPhraseList()   # get all phrases in this part

         # loop through all the phrases in the part
         for phrase in phrases:
            currentTime = phrase.getStartTime()   # update current time to note's start time

            if self.TEST_OUTPUT:
               print("Phrase starts at: " + str(currentTime))

            # add all the notes of the current phrase to our note vector, keeping track of their start time
            for n in range(phrase.getSize()):
               note = phrase.getNote(n)

               if not note.isRest():   # if this is an actual note...
                  # ...add note and its start time in the list of notes
                  allNoteArray.append(ExtendedNote(note, currentTime))

                  if self.TEST_OUTPUT:
                     print("Added note: start time: " + str(currentTime))

               currentTime += note.getLength()   # update the current time to note's end time (length = performance time)

      # now, all notes are contained within our note vector.

      # If score is empty, then a null piano roll would be created -
      # better to just exit now
      if len(allNoteArray) == 0:
         raise AssertionError("Score is empty!")

      # If score contains only one note, create Piano Roll but
      # print out an warning since this very atypical
      if len(allNoteArray) == 1:
         print("PianoRoll(): Warning!  Score contains only one note...")

      # Sort note array--
      # array primary sort: start time
      # array seconday sort: pitch
      # (contained in ExtendedNote class)
      allNoteArray.sort()

      # add an empty element at index 0 -- the first position will not be used,
      # since note continuation is signified by negative indices -- 0 cannot have
      # a negative sign.
      finalArray = [None] + allNoteArray

      # now, the note array has been created, sorted, and has an empty first element.

      return finalArray

   def _populatePianoRoll(self, notes, quantum, scoreEndTime):
      """
      This method populates the piano roll with the notes from the notes[] array.
      It traverses the sorted note array and adds each note to the proper
      "time slice" of the piano roll. If the note is at least the length (duration) of a quantum,
      it is included. By "inclusion" it is meant that the index of the note in the note
      array is placed in a corresponding timeslice. If the note begins to sound in the current
      timeslice then the index is positive. If it continues to sound past the current time slice, then each subsequent
      time slice in which it sounds contains the negated index of the note (this is to signify
      that it is merely "still sounding" or is a rest from a note that started in an earlier time slice).
      A note index of a note is only added into a timeslice if the pitch of that note is not already included in the timeslice.
      This is due to that a pianoroll does not distinguish two notes of the same pitch that sound at the same time. When
      two notes with the same pitch overlap, the start note that starts during the prior note is represented as if it
      started after (but directly adjacent to) the end of this prior note.

      For each note encountered, it is entered in the appropriate time slice (given the note's start time)
      and then we "look forward" adding negative indices to time slices until we reach the end time of the note.
      Then we repeat the process for the next note.

      param list[ExtendedNote] notes: an array of notes
      param float quantum: the duration of each time slice
      param float scoreEndTime: the end time of the score
      return list[list[int]]: a piano roll representation of the score
      """
      currentTime = 0.0   # keeps track of the time (in quantum leaps)

      NEW_NOTE = False         # denotes a new note
      CONTINUED_NOTE = True    # denotes a note continuation

      # derive the raster scores total length
      numTimeSlices = scoreEndTime / quantum
      rasterLength = math.ceil(numTimeSlices)

      if self.TEST_OUTPUT:
         print(" quantum = " + str(quantum) + "; scoreEndTime " + str(scoreEndTime))
         print(" timeSlice duration (quantum) = " + str(quantum))
         print("rasterLength = " + str(rasterLength))

      # let's construct the pianoRoll (raster score to be returned)
      pianoRoll = [[] for _ in range(rasterLength)]

      # ensure that they are not using up too much space
      if rasterLength > 32767 * 4:   # Short.MAX_VALUE in Java is 32767
         print("PianoRoll(): Warning...  given this Score, a quantum of " + str(quantum) +
               " creates a PianoRoll with " + str(rasterLength) + " time slices.  This may use up too much space...")

      # populate the piano roll:
      # for every time slice in the piano roll...
      noteIndex = 1   # holds current position within the note array; skip first (unused) element
      for timeSlice in range(rasterLength):
         # populate this time slice...
         # while we have another note whose start time is within this time slice
         while noteIndex < len(notes) and notes[noteIndex].getStartTime() < currentTime + quantum:
            # drop notes whose duration is smaller than a quantum

            if notes[noteIndex].getLength() >= quantum:   # length = performance time
               noteStartAlreadyAdded = False   # starting with note's first timeslice

               # get the pitch of the note being inserted
               thisNotesPitch = notes[noteIndex].getPitch()   # holds pitch of the note being inserted

               # does this same pitch already exist in this timeSlice?
               # notes are only inserted into a timeSlice if the same pitch doesn't already exist
               pitchExistsInTimeSlice = self._isTherePitch(pianoRoll[timeSlice], thisNotesPitch)

               # if this same pitch does NOT already exist in this timeSlice,
               # add beginning of this note into this timeslice (dynamic allocation)
               if not pitchExistsInTimeSlice:
                  pianoRoll[timeSlice] = self._expandTimeSlice(pianoRoll[timeSlice], noteIndex, NEW_NOTE)
                  noteStartAlreadyAdded = True   # keep track if this note's start was added into the pianoroll
                                                 # if not, we need to add a start (positive index) of this note
                                                 # when looking into future timeslices instead of a continuation

               if self.TEST_OUTPUT:
                  en = self.getNote(noteIndex)
                  print("\npianoRoll[" + str(timeSlice) + "] Start: " + str(en.getStartTime()) +
                             " Pitch: " + str(en.getPitch()) + " Length: " + str(en.getLength()) +
                             " Duration: " + str(en.getDuration()))
                  print("pianoRoll[" + str(timeSlice) + "][" + str(len(pianoRoll[timeSlice])-1) +
                             "] = " + str(noteIndex))

               # Now add the negated note index to each future time slice the note continues to sound in.
               # (Recall that we use negative note indices in time slices to indicate
               # that a note started in an earlier time slice.)

               futureTimeSlice = 0        # points to future time slices
               startOfNextQuantum = 0.0   # holds time limit for deciding if a note belongs in a future time slice
               noteEndTime = 0.0          # holds a note's end time

               futureTimeSlice = timeSlice + 1            # points to next time slice
               startOfNextQuantum = currentTime + quantum   # start time of next time slice
                                                            # (rests that don't reach into the next timeSlice are dropped because they are less than a quantum)

               # while there is a future time slice and the note continues to "sound",
               # consider adding continuations of this note into the future time slices.
               noteEndTime = currentTime + notes[noteIndex].getLength()   # length = performance time
               while noteEndTime > startOfNextQuantum and futureTimeSlice < rasterLength:
                  # does this same pitch already exist in this timeSlice?
                  pitchExistsInTimeSlice = self._isTherePitch(pianoRoll[futureTimeSlice], notes[noteIndex].getPitch())

                  # if this same pitch does NOT already exist in this timeSlice,
                  # add relevant part of this note into this future timeslice
                  if not pitchExistsInTimeSlice:
                     # if a start index for this note is already in the pianoroll, add a continuation
                     if noteStartAlreadyAdded:
                        pianoRoll[futureTimeSlice] = self._expandTimeSlice(pianoRoll[futureTimeSlice], noteIndex, CONTINUED_NOTE)
                     else:   # otherwise add a start for this note here
                        pianoRoll[futureTimeSlice] = self._expandTimeSlice(pianoRoll[futureTimeSlice], noteIndex, NEW_NOTE)
                        noteStartAlreadyAdded = True

                  # point to next future time slice
                  futureTimeSlice += 1
                  startOfNextQuantum += quantum
               # end adding note "continuations" into future timeslices

               # now, futureTimeSlice points to the timeslice directly after the end of the current note

               # set the quantized start time of the current note...
               notes[noteIndex].setStartTimeQuantized(currentTime)

               # calculate and set the quantized duration of the current note...
               noteDurationQuantized = (futureTimeSlice - timeSlice) * quantum
               notes[noteIndex].setDurationQuantized(noteDurationQuantized)

               if self.TEST_OUTPUT:
                  print(" Start quantized: " + str(en.getStartTimeQuantized()) +
                             " Duration quantized: " + str(noteDurationQuantized))

            # done adding a note (we only add notes that are longer than the quantum)

            noteIndex += 1   # point to next note in the note array

         # done populating this time slice

         # moving onto the next time slice (while loop)
         currentTime += quantum
      # done populating the piano roll (for loop)

      return pianoRoll

   def _expandTimeSlice(self, timeSlice, noteIndex, continuation):
      """
      Inserts a note into a time slice based on pitch, in increasing order.

      Precondition: Pitch should not already exist in this time slice.

      param list[int] timeSlice: a time slice to be expanded by one note
      param int noteIndex: the note's index in the note array
      param bool continuation: indicates if the note is a continuation or should be added as to start "time slice"
      return list[int]: the time slice with the new index appended (new note inserted)
      """
      tempSlice = [0] * (len(timeSlice) + 1)   # holds the time slice (with one extra spot for the new note)
      newNotePitch = self.getNote(abs(noteIndex)).getPitch()

      index = 0

      # copy existing notes with pitch < newNotePitch
      while index < len(timeSlice) and self.getNotesPitchFromSlice(index, timeSlice) < newNotePitch:
         tempSlice[index] = timeSlice[index]
         index += 1

      # now, index points to place of insertion

      # insert index of the new note in timeSlice
      if continuation:   # is this a continued note?
         tempSlice[index] = -noteIndex   # yes, so negate its index
      else:
         tempSlice[index] = noteIndex   # no, so store it as is

      index += 1

      # copy remaining existing notes (if any)
      while index < len(tempSlice):
         tempSlice[index] = timeSlice[index - 1]
         index += 1

      return tempSlice   # return expanded time slice

   def _isTherePitch(self, timeSlice, pitch):
      """
      Determines whether the pitch passed to the parameter already exists in the timeslice passed to the parameter.

      param list[int] timeSlice: the timeslice to be searched for the pitch
      param int pitch: the pitch to be searched for in the timeslice
      return bool: true if the pitch was found in the timeslice, false otherwise
      """
      found = False
      moreToSearch = True

      index = 0

      while index < len(timeSlice) and moreToSearch:
         if self.getNotesPitchFromSlice(index, timeSlice) >= pitch:
            moreToSearch = False   # early out if passed or at where pitch would be in the timeSlice

            if self.getNotesPitchFromSlice(index, timeSlice) == pitch:   # if pitch is in the timeSlice
               found = True
         index += 1

      return found

   def getNote(self, index):
      """
      Returns the note of the music piece at index position passed to parameter.  First note is stored at index 1
      (not 0).

      param int index: the index of the note in the PianoRoll.
      return ExtendedNote: the corresponding note from the Score.  This is the original, un-quantized note.
      """
      return self.noteArray[index]

   def getNotesPitchFromSlice(self, notePosition, timeSlice):
      """
      Returns a Note's pitch. Same as getNotesPitch(int,int), only this one is passed the actual timeslice.

      param int notePosition: the position of the desired Note in the timeslice
      param list[int] timeSlice: the actual time slice in which the desired Note is found
      return int: the pitch of the indicated note in the indicated timeslice, -1
               if the notePosition is greater than the length of the timeslice.
      """
      return self.getNote(abs(timeSlice[notePosition])).getPitch()   # return the note's pitch

   def _assignRollVoices(self, pianoRoll):
      """
      Assigns voices to each note in the note array.
      Determines where all the contigs begin and end, and keeps
      track of the max contigs. Upon completion, 'noteArray' notes will have
      been assigned voices that more or less follow voicing assignment rules from music theory.

      Note:  This algorithm is inspired from "Separating Voices in Polyphonic Music:
             A Contig Mapping Approach" by Elaine Chew and Xiaodan Wu
             http://www-rcf.usc.edu/~echew/ papers/CMMR2004/ecxw-cmmr2004.pdf

      Precondition: 'pianoRoll' contains time slices of the notes in 'noteArray'
                    No 'pianoRoll' time slice is larger than 16 notes (limit imposed
                    by available MIDI voices/channels).

      param list[list[int]] pianoRoll: the two dimensional array representing the pianoroll
      """

      contigList = []   # contains all contigs in the order
                        # ...that they appear in the pianoRoll

      # identify where the contigs begin and end
      self._findContigs(contigList)

      # assigns optimal (hopefully) voices to contigs
      self._assignContigVoices(contigList)

      # now, all contigs have been voiced, creating islands (neighborhoods)
      # of consistent, fluid (linear) voicings.  However, where these islands meet
      # we may have discontinuities (fragmentation) in voicing.

      # align voices in contig islands so that we end up with one island
      # (neighborhood) of consistent, fluid (linear) voicings.
      # *** To do..
      # Note: This is similar to similar to the above, only at a higher level,
      # ...id est, findIslands(), assignIslandVoices()
      #??alignContigNeighborhoods(contigList);

      # assign voices to notes in noteArray using voice info in contigList
      self._copyContigVoicesToRoll(contigList)

      if self.TEST_OUTPUT:
         self.contigAndVoicePrintout(contigList)

   def _copyContigVoicesToRoll(self, contigList):
      """
      Copies the voices in each contig to each note within
      the timeslices contained by the contigue. Every note will contain a voice.
      (This is assuming that each contig has a voice for each layer of the timeslices.
      It is possible that propogateContigVoices did not voice a layer. In this case,
      the note will not be voiced. See the documentation for that method.)

      Precondition: Every contig in the contigList has been voiced.

      param list[Contig] contigList: a list that represents the listing of pianoRoll's contig's
      """
      tempContig = None
      voices = []
      startIndex = 0
      endIndex = 0
      tempNote = None
      timeslice = []

      # for each contig
      for count in range(len(contigList)):
         tempContig = contigList[count]
         voices = tempContig.getVoicesArray()
         startIndex = tempContig.start
         endIndex = tempContig.end

         # for each time slice in the contig
         for sliceCount in range(startIndex, endIndex + 1):

            # get the current timeslice
            timeslice = self.getTimeSlice(sliceCount)

            # for each voice (iterate through voices from contig rather than
            # by size of timeslice - there's a chance that one or more voice values
            # in the contig were not filled).
            for voiceCount in range(len(voices)):
               # take it one note at time - only look at note if it has
               # just begun to sound (an index greater than 0) - otherwise
               # it has already been set.
               if timeslice[voiceCount] > 0:
                  tempNote = self.getNote(timeslice[voiceCount])
                  tempNote.setVoice(voices[voiceCount])

   def _findContigs(self, contigList):
      """
      Goes through the pianoRoll and identifies the start
      and end indices of all contigs found in pianoroll and adds them to the contigList.
      It looks for a change in the number of voices, as well as any large
      changes in a voices pitch that would necessitate using a voice
      that is not in the current contig.

      param list[Contig] contigList: a list that represents the listing of pianoRoll's contig's
      """
      pianoRollSize = self.getLength()   # length of piano roll
      startIndex = 0                     # index of first slice in current contig
      tempContig = None                  # temporary contig object
      pianoRollIndex = 0                 # used to traverse pianoRoll

      for pianoRollIndex in range(1, pianoRollSize):
         # check to see if current position is a new contig
         if self._isNewContig(pianoRollIndex, pianoRollIndex - 1):
            tempContig = Contig(startIndex, pianoRollIndex - 1, len(self.getTimeSlice(pianoRollIndex - 1)))
            contigList.append(tempContig)
            startIndex = pianoRollIndex   # remember beginning of new contig

      # we need to add everything from the last startIndex up until
      # the end of the piano roll to the contig list
      tempContig = Contig(startIndex, pianoRollIndex, len(self.getTimeSlice(pianoRollIndex)))
      contigList.append(tempContig)

   def _isNewContig(self, firstIndex, secondIndex):
      """
      Checks the two timeslices indicated by the indices given
      to see if the second timeslice should be a part of a new contig (indicated
      by a larger second slice or by excessive change in a voices pitch).

      param int firstIndex: the index of the first timeslice
      param int secondIndex: the index of the second timeslice
      return bool: true if there should be a new contig, false otherwise
      """
      firstSlice = self.getTimeSlice(firstIndex)
      secondSlice = self.getTimeSlice(secondIndex)
      returnValue = False      # return value
      pitchDifference = 0      # temporary value holding change in pitch
                               # ..in a voice between the two time slices.
                               # ..initialize to 0

      noteOne = None           # these are used to temporarily hold notes
      noteTwo = None           # ..from the noteArray

      # if the slices are different in size, we found a new contig
      if len(firstSlice) != len(secondSlice):
         returnValue = True

      # else they are the same size; ergo, we must examine both,
      # checking each voice's change in pitch to make sure it has
      # not exceeded MAX_VOICE_JUMP.
      else:
         excessivePitchChange = False   # true, if we found a break in voice; else, false

         sliceIndex = 0   # points to a position (pair of notes) in both timeSlices

         # while there are still notes in the two timeSlice arrays
         # and we have not yet found a break in any voice
         while sliceIndex < len(firstSlice) and not excessivePitchChange:
            # must get absolute value of index because continuations are negative
            noteOne = self.getNote(abs(firstSlice[sliceIndex]))
            noteTwo = self.getNote(abs(secondSlice[sliceIndex]))

            pitchDifference = abs(noteOne.getPitch() - noteTwo.getPitch())   # calculate voice jump
            if pitchDifference > self.maxVoiceJump:
               excessivePitchChange = True
            sliceIndex += 1

         # if there is an excessivePitchChange then return true,
         # else return false
         returnValue = excessivePitchChange

      return returnValue

   def _assignContigVoices(self, contigList):
      """
      Assigns voices to the contigs found in the pianoRoll, with the aim that 'contigList' contains consistent, fluid (linear) voicings.

      param list[Contig] contigList: a list that represents the listing of pianoRoll's contig's
      """
      i = 0                  # points to a contig in contigList
      maxContigIndex = 0     # points to the leftmost max contig in contigList

      # Find each max unvoiced contig, voice it, and propagate
      # voices as much as possible to the left and right.
      # Repeat until there are no more unvoiced contigs.

      # find first contig to work with (if any)
      maxContigIndex = self._findLeftmostMaxUnvoicedContig(contigList)
      while maxContigIndex != -1:   # more left to do?

         # assign voices to max contig using strategy of choice
         self._voiceMaxContig(contigList[maxContigIndex])

         if self.TEST_OUTPUT:
            print("max contig (" + str(maxContigIndex) + ") to string:\n" + str(contigList[maxContigIndex]))
            print("STARTING: Assigning voices to maxContig(" + str(maxContigIndex) + ") neighborhood...")

         # assign voices to the left and right of max contig
         self._voiceMaxContigNeighborhood(contigList, maxContigIndex)

         if self.TEST_OUTPUT:
            print("ENDING: Assigning voices...")

         # find next contig to work with (if any)
         maxContigIndex = self._findLeftmostMaxUnvoicedContig(contigList)

      # now, all contigs have been voiced, creating islands (neighborhoods)
      # of consistent, fluid (linear) voicings.  However, where these islands meet
      # we may have discontinuities in voicing.

   def _voiceMaxContig(self, maxContig):
      """
      Assigns voices arbitrarily starting at the
      bottom of the maxContig and moving upward, from 0 up to the end
      of the voice vector.

      param Contig maxContig: a maxContig created with the proper number of voices
      """
      voices = []

      # update the maximum number of voices in the PianoRoll
      if self.numberOfVoices < maxContig.numVoices():
         self.numberOfVoices = maxContig.numVoices()

      for i in range(maxContig.numVoices()):
         voices.append(i)

      maxContig.voices = voices
      maxContig.voiced = True

   def _voiceMaxContigNeighborhood(self, contigList, maxContigIndex):
      """
      Assigns voices in a found maxContig's neighborhood. A contig neighborhood is defined as a sequence
      of contigs left and right of 'contigList[maxContigIndex]' which are unvoiced, they are
      progressively shrinking (in terms of number of voices) as you move away from
      'contigList[maxContigIndex]'.

      Precondition:  'contigList[maxContigIndex]' is voiced

      Note: A contig neighborhood is defined as a sequence of contigs left and right
            of 'contigList[maxContigIndex]' which are unvoiced, they are progressively
            shrinking (in terms of number of voices) as you move away from
            'contigList[maxContigIndex]'.

      param list[Contig] contigList: a list that represents the listing of pianoRoll's contig's
      param int maxContigIndex: the index of the maxContig
      """
      i = 0                           # points to a contig index
      unvoiced = []                   # temporary lists
      voiced = []
      unvoicedTSindex = 0             # time slice indicies
      voicedTSindex = 0

      if self.TEST_OUTPUT:
         print("starting to voice contig  neighborhood")

      # assign voices to the left
      i = maxContigIndex - 1
      while (i >= 0 and
             self._isUnvoiced(contigList[i]) and
             self._isSmaller(contigList[i], contigList[i + 1])):

         # assign voices to contigList[i] based on voices in contigList[i+1]
         unvoiced = contigList[i].voices                  # voices of unvoiced contig
         voiced = contigList[i + 1].voices                # voices of voiced contig
         unvoicedTSindex = contigList[i].end              # pianoroll index of unvoiced contig
         voicedTSindex = contigList[i + 1].start          # pianoroll index of voiced contig

         if self.TEST_OUTPUT:
            print("about to voice contig " + str(i))

         # assign voices to unvoiced contig
         contigList[i].voices = self._propagateContigVoices(unvoiced, 0, unvoicedTSindex, voiced, 0, voicedTSindex)
         contigList[i].voiced = True

         if self.TEST_OUTPUT:
            print("Just voiced contig " + str(i))

         i -= 1

      # assign voices to the right
      i = maxContigIndex + 1
      while (i < len(contigList) and
             self._isUnvoiced(contigList[i]) and
             self._isSmaller(contigList[i], contigList[i - 1])):

         # assign voices to contigList[i] based on voices in contigList[i-1]
         unvoiced = contigList[i].voices                  # voices of unvoiced contig
         voiced = contigList[i - 1].voices                # voices of voiced contig
         unvoicedTSindex = contigList[i].start            # pianoroll index of unvoiced contig
         voicedTSindex = contigList[i - 1].end            # pianoroll index of voiced contig

         # assign voices to unvoiced contig
         contigList[i].voices = self._propagateContigVoices(unvoiced, 0, unvoicedTSindex, voiced, 0, voicedTSindex)
         contigList[i].voiced = True

         if self.TEST_OUTPUT:
            print("Just voiced contig " + str(i))

         i += 1

   def _findLeftmostMaxUnvoicedContig(self, contigList):
      """
      Finds the leftmost unvoiced maxContig.  A maxContig is defined as having the
      most number of voices within it that the voicing algorithm has seen.

      param list[Contig] contigList: a list that represents the listing of pianoRoll's contig's
      return int: index of the found maxContig
      """
      maxContigIndex = -1   # Keep track of the max contig's index.
                            # ...Start with index of -1, which is what
                            # ...we'll return if there are no more unvoiced
                            # ...contigs left.

      maxSize = 0           # Keep track of max contigs size.

      tempContig = None     # Temporary contig used for iteration.

      for i in range(len(contigList)):
         tempContig = contigList[i]

         # If current contig is the biggest we've come across and is unvoiced
         # ...assign its index to maxContigIndex
         if self._isUnvoiced(tempContig) and tempContig.numVoices() > maxSize:
            maxContigIndex = i
            maxSize = tempContig.numVoices()

      return maxContigIndex

   def _isUnvoiced(self, contig):
      """
      Checks a contig to see if it has been voiced or not.

      param Contig contig: the contig to be checked
      return bool: true if contig is not voiced, true if voiced.
      """
      return not contig.voiced

   def _isSmaller(self, smallContig, bigContig):
      """
      This method compares the first contig to the second.  If the first contig is
      smaller than the second, the method returns true.  It returns false if the
      second is larger.

      param Contig smallContig: the first contig to compare
      param Contig bigContig: the second contig to compare
      return bool: true if first contig is smaller
      """
      return smallContig.numVoices() < bigContig.numVoices()

   def _propagateContigVoices(self, unvoiced, firstUnvoicedIndex, unvoicedTSindex,
                             voiced, firstVoicedIndex, voicedTSindex):
      """
      Assigns voices to the first contig based on the already assigned voices
      in the second contig. The first contig will always be smaller than the second.

      param list[int] unvoiced: available voice slots in unvoiced contig
      param int firstUnvoicedIndex: timeSlice index of note corresponding to first available voice slot
      param int unvoicedTSindex: index of time slice corresponding to unvoiced contig
      param list[int] voiced: voices to be used for voicing of unvoiced contig
      param int firstVoicedIndex: timeSlice index of note corresponding to first voice to be propagated
      param int voicedTSindex: index of time slice corresponding to voiced contig
      return list[int]: the best voice assignment for the unvoiced contig
      """
      returnValue = []   # vector that will be returned
      alt1 = []          # vectors that hold temporary values
      alt2 = []

      if len(unvoiced) == 0:   # base case
         returnValue = unvoiced   # no voice assignments possible

      elif len(unvoiced) == len(voiced):   # base case
         returnValue = voiced                # only one possible voice assignment

      else:   # len(unvoiced) < len(voiced)
         # try alternative voicings
         # keep first voice, get best voice assignment given rest of lists
         alt1 = self._cons(self._car(voiced),
                          self._propagateContigVoices(self._cdr(unvoiced), firstUnvoicedIndex + 1, unvoicedTSindex,
                                                     self._cdr(voiced), firstVoicedIndex + 1, voicedTSindex))

         # skip first voice, get best voice assignment from rest of voices
         alt2 = self._propagateContigVoices(unvoiced, firstUnvoicedIndex, unvoicedTSindex,
                                           self._cdr(voiced), firstVoicedIndex + 1, voicedTSindex)

         # keep the best voice assignment in terms of shortest distance traveled by voices
         returnValue = self._bestVoiceAssignment(alt1, alt2, firstUnvoicedIndex, voiced, firstVoicedIndex, unvoicedTSindex, voicedTSindex)

      return returnValue

   def _car(self, v):
      """
      Returns the first object in the vector. (Inspired by the car method in Lisp.)

      param list v: a list
      return: first object in the list
      """
      return v[0]

   def _cdr(self, v):
      """
      Returns a vector containing all entries in the vector passed to parameter except for the first.
      (Inspired by the cdr method in Lisp.)

      param list v: a list
      return list: a new list containing all entries except the first one
      """
      if len(v) != 0:
         return v[1:]      # return slice from index 1 to end
      else:
         return []         # return empty list

   def _cons(self, first, rest):
      """
      Returns a newly constructed vector using data from another vector and a new object as its
      first entry.

      param first: the first object in the new list
      param list rest: the list with the rest of the data
      return list: the newly constructed list
      """
      return [first] + rest

   def _bestVoiceAssignment(self, unvoicedAlt1, unvoicedAlt2, firstUnvoicedIndex,
                           voiced, firstVoicedIndex, unvoicedTSindex, voicedTSindex):
      """
      Gets the distance between each note pitch in the unvoicedTSindex, and the corresponding
      one (wrt voice assignment) in voicedTSindex.  The summation of the pitch distances for each voice assignment,
      alt1 and alt2, determines which voice assignment to return.
      This method returns the best voice assignment (either unvoicedAlt1 or unvoicedAlt2) as compared to
      the voicing in "voiced".

      Precondition:  len(unvoicedAlt1) == len(unvoicedAlt2) and len(unvoicedAlt2) < len(voiced)
                     Each voice ID in the unvoiced vectors is present in the voiced one.

      param list[int] unvoicedAlt1: one possible voice assignment for part of the unvoiced contig
      param list[int] unvoicedAlt2: another possible voice assignment for part of the unvoiced contig
      param int firstUnvoicedIndex: timeSlice index of note corresponding to first available voice slot
      param list[int] voiced: voices to be used for voicing of unvoiced contig
      param int firstVoicedIndex: timeSlice index of note corresponding to first voice to be propagated
      param int unvoicedTSindex: index of time slice corresponding to unvoiced contig
      param int voicedTSindex: index of time slice corresponding to voiced contig
      return list[int]: the best voice assignment (either unvoicedAlt1 or unvoicedAlt2) as compared to
                         the voicing in "voiced"
      """
      pitchDifferenceAlt1 = 0
      pitchDifferenceAlt2 = 0
      voice = 0

      if self.TEST_OUTPUT:
         print("---------> within bestVoiceAssignment()")

      # iterate through all voice assignments for first alternative
      for i in range(len(unvoicedAlt1)):
         voice = unvoicedAlt1[i]                                                  # get proposed voice assignment for this note
         absIndex = firstUnvoicedIndex + i                                        # calculate index relative to the beginning of the unvoice contig
         pitchDifferenceAlt1 += abs(self._getNotesPitch(absIndex, unvoicedTSindex)                    # accumulate difference between pitch of this note
                                    - self._getVoicesPitch(voice, voiced, firstVoicedIndex, voicedTSindex))   # ...and pitch of the voiced note having same voice

      # iterate through all voice assignments for second alternative
      for i in range(len(unvoicedAlt2)):
         voice = unvoicedAlt2[i]                                                  # get proposed voice assignment for this note
         absIndex = firstUnvoicedIndex + i                                        # calculate index relative to the beginning of the unvoice contig
         pitchDifferenceAlt2 += abs(self._getNotesPitch(absIndex, unvoicedTSindex)                    # accumulate difference between pitch of this note
                                    - self._getVoicesPitch(voice, voiced, firstVoicedIndex, voicedTSindex))   # ...and pitch of the voiced note having same voice

      if self.TEST_OUTPUT:
         print("Alt1 = " + str(unvoicedAlt1) + "; pitchDifferenceAlt1 = " + str(pitchDifferenceAlt1))
         print("Alt2 = " + str(unvoicedAlt2) + "; pitchDifferenceAlt2 = " + str(pitchDifferenceAlt2))

      if pitchDifferenceAlt1 > pitchDifferenceAlt2:
         return unvoicedAlt2
      else:
         return unvoicedAlt1

   def _getVoicesPitch(self, voice, voiced, firstVoicedIndex, voicedTSindex):
      """
      This method is given a voice, a vector containing voices, and
      an index to the piano roll. It finds the specified voice in the
      voiced vector, then it uses the index of the voice to access the
      corresponding note in the timeSlice. Finally, it returns the pitch
      of that note.

      Note: The vector and the timeslice are parallel arrays.

      Precondition: The timeslice being passed MUST already be voiced!
                    Also, the voice must be contained within the vector.

      param int voice: the voice of the note we are trying to locate in the voiced contig
      param list[int] voiced: the voiced contig
      param int firstVoicedIndex: timeSlice index of note corresponding to first entry in voiced contig
      param int voicedTSindex: index of time slice corresponding to voiced contig
      return int: the pitch of the note located
      """
      timeslice = self.getTimeSlice(voicedTSindex)
      index = 0            # index to timeslice
      noteVoice = 0        # holds a voice from the voice vector
      found = False        # true if we found the voice; false otherwise

      # traverse the voiced vector until we find the voice that matches
      # the one we were given
      index = 0
      found = False   # voice has not been found yet
      while index < len(voiced) and not found:
         noteVoice = voiced[index]   # get next voice

         if noteVoice == voice:   # did we find it?
            found = True          # ...yes, so remember that
         else:
            index += 1            # ...no, so keep looking

      # Now, if 'found' then 'index points to the position in the timeSlice of the note
      # ...associated with the given voice.
      # Otherwise we have violated our precondition -- the voice we are looking is
      # NOT in the the voiced vector, so catch that
      assert found, " Voiced vector " + str(voiced) + " does not contain voice " + str(voice)

      #testing//
      #print("Voice " + str(voice) + " is located at " + str(index) + " in voiced contig " + str(voiced))
      #////////

      # return the pitch of this note -- adjust for cropping of voiced contig
      return self._getNotesPitch(firstVoicedIndex + index, voicedTSindex)

   def _getNotesPitch(self, notePosition, timeIndex):
      """
      Returns the pitch of the Note at notePosition and timeIndex passed to parameter.

      Precondition: notePosition > (len(timeSlice) - 1)

      param int notePosition: the position of the desired Note in the timeslice
      param int timeIndex: the index of the timeslice in which the desired Note is located
      return int: the pitch of the indicated note in the indicated timeslice, -1
                   if the notePosition is greater than the length of the timeslice.
      """
      timeSlice = self.getTimeSlice(timeIndex)   # get corresponding timeSlice

      return self.getNote(abs(timeSlice[notePosition])).getPitch()   # return the note's pitch

   def getTimeSlice(self, timeIndex):
      """
      Returns a specific time slice from the PianoRoll representation.

      param int timeIndex: the time index of the desired time slice to be returned.
      return list[int]: the time slice at time index, represented as an array of shorts, each of which is a note identifier.
      """
      return self.pianoRoll[timeIndex]

   def getLength(self):
      """
      Returns the number of time slices in the PianoRoll representation.

      return int: the number of time slices in the PianoRoll representation.
      """
      return len(self.pianoRoll)

   def getNoteCount(self):
      """
      Returns the number of notes in the score.

      return int: the number of notes in the score
      """
      return len(self.noteArray) - 1   # index 0 is not used, thus -1

   def getQuantum(self):
      """
      Returns the quantum of the PianoRoll representation.  Once a PianoRoll is created,
      it's quantum cannot be changed, so no setQuantum function is provided.

      return float: the quantum of time slices in the PianoRoll representation.
      """
      return self.quantum

   def getNumVoices(self):
      """
      Returns number of voices assigned to the score.

      return int: the number of voices assigned to the score
      """
      return self.numberOfVoices

   def getNextNoteSameVoice(self, voice, timeIndex):
      """
      Returns the first note in a future time slice that is in
      the given voice.

      param int voice: the voice of the note to be found
      param int timeIndex: the index of the current time slice
      return ExtendedNote: the next note in the voice if one exists, None otherwise
      """
      found = False   # note has not been found yet
      nextNote = None

      timeIndex += 1   # begin search in the future
      while timeIndex < self.getLength() and not found:   # while next note is not found and there are more time slices left
         timeSlice = self.getTimeSlice(timeIndex)   # get timeslice
         index = 0   # start at the first note in this time slice (if any)
         while index < len(timeSlice) and not found:   # while next note is not found and still notes within this time slice
            if timeSlice[index] > 0:   # if a new note found
               nextNote = self.getNote(timeSlice[index])   # check this note
               if voice == nextNote.getVoice():   # if voices match...
                  found = True   # ...we are done!
            index += 1   # point to another note (if any)
         # postcondition: we either found the note, or this time slice is finished

         timeIndex += 1   # point to next time slice (if any)
      # postcondition: we either found the note, or the piano roll is finished

      # if we looked through the whole piano roll and did not find
      # the note we were looking for, return None
      if not found:
         nextNote = None

      return nextNote

   def getNextNoteSamePitch(self, pitch, timeIndex):
      """
      Returns the first note in a future time slice that has the given pitch.

      param int pitch: the pitch of the note to be found
      param int timeIndex: the index of the current time slice
      return ExtendedNote: the next note matching the pitch if one exists, or None
      """
      found = False   # note has not been found yet
      nextNote = None

      timeIndex += 1   # begin search in the future
      while timeIndex < self.getLength() and not found:   # while next note is not found and there are more time slices left
         timeSlice = self.getTimeSlice(timeIndex)   # get timeslice
         index = 0   # start at the first note in this time slice (if any)
         while index < len(timeSlice) and not found:   # while next note is not found and still notes within this time slice
            if timeSlice[index] > 0:   # if a new note found
               nextNote = self.getNote(timeSlice[index])   # check this note
               if pitch == nextNote.getPitch():   # if pitches match...
                  found = True   # ...we are done!
            index += 1   # point to another note (if any)
         # postcondition: we either found the note, or this time slice is finished

         timeIndex += 1   # point to next time slice (if any)
      # postcondition: we either found the note, or the piano roll is finished

      # if we looked through the whole piano roll and did not find
      # the note we were looking for, let them know...
      if not found:
         nextNote = None

      return nextNote

   def getNextNoteSameDuration(self, duration, timeIndex):
      """
      Returns the first note in a future time slice that has the given duration.

      param float duration: the duration of the note to be found
      param int timeIndex: the index of the current time slice
      return ExtendedNote: the next note matching the duration if one exists, or None
      """
      found = False   # note has not been found yet
      nextNote = None

      timeIndex += 1   # begin search in the future
      while timeIndex < self.getLength() and not found:   # while next note is not found and there are more time slices left
         timeSlice = self.getTimeSlice(timeIndex)   # get timeslice
         index = 0   # start at the first note in this time slice (if any)
         while index < len(timeSlice) and not found:   # while next note is not found and still notes within this time slice
            if timeSlice[index] > 0:   # if a new note found
               nextNote = self.getNote(timeSlice[index])   # check this note
               if duration == nextNote.getLength():   # length = performance time
                  found = True   # ...we are done!
            index += 1   # point to another note (if any)
         # postcondition: we either found the note, or this time slice is finished

         timeIndex += 1   # point to next time slice (if any)
      # postcondition: we either found the note, or the piano roll is finished

      # if we looked through the whole piano roll and did not find
      # the note we were looking for, let them know...
      if not found:
         nextNote = None

      return nextNote

   def getNextNoteSameDurationQuantized(self, durationQuantized, timeIndex):
      """
      Returns the first note in a future time slice that has the given quantized duration.

      param float durationQuantized: the quantized duration of the note to be found
      param int timeIndex: the index of the current time slice
      return ExtendedNote: the next note matching the duration if one exists, or None
      """
      found = False   # note has not been found yet
      nextNote = None

      timeIndex += 1   # begin search in the future
      while timeIndex < self.getLength() and not found:   # while next note is not found and there are more time slices left
         timeSlice = self.getTimeSlice(timeIndex)   # get timeslice
         index = 0   # start at the first note in this time slice (if any)
         while index < len(timeSlice) and not found:   # while next note is not found and still notes within this time slice
            if timeSlice[index] > 0:   # if a new note found
               nextNote = self.getNote(timeSlice[index])   # check this note
               if durationQuantized == nextNote.getDurationQuantized():   # if rhythms match...
                  found = True   # ...we are done!
            index += 1   # point to another note (if any)
         # postcondition: we either found the note, or this time slice is finished

         timeIndex += 1   # point to next time slice (if any)
      # postcondition: we either found the note, or the piano roll is finished

      # if we looked through the whole piano roll and did not find
      # the note we were looking for, let them know...
      if not found:
         nextNote = None

      return nextNote

   def _timeSliceContainsNote(self, timeSliceIndex, noteIndex):
      """
      Given the index of a timeSlice and the note's position in the note array,
      this method will determine if the given timeSlice contains the given note.
      It will return True both if the note has just begun to sound in the
      timeslice or is a continuation in the timeslice.

      Precondition: The pianoRoll is populated and contains the given index.
                    Also, the ExtendedNoteArray is populated and contains the
                    given index.

      param int timeSliceIndex: the index of a timeslice in the pianoroll
      param int noteIndex: the index in the note array of the note to look for
      return bool: whether or not the timeslice contained the note
      """
      timeSlice = self.getTimeSlice(timeSliceIndex)
      index = 0
      doesContain = False

      while index < len(timeSlice) and not doesContain:
         if abs(timeSlice[index]) == abs(noteIndex):
            doesContain = True
         index += 1

      return doesContain

   def _getNotesEnd(self, startTimeSliceIndex, noteIndex):
      """
      Given the index of the first timeslice that a note sounds in and the note's
      position in the note array, this method will find the index of the last
      timeSlice that it sounds in.

      param int startTimeSliceIndex: the timeslice at which the note starts
      param int noteIndex: the index of the note in the note array
      return int: the last timeslice the note sounds in
      """
      rasterLength = self.getLength()   # holds length of PianoRoll
      isSounding = True   # true if note is sounding; false otherwise

      endTimeSliceIndex = startTimeSliceIndex + 1   # initialize

      # traverse the PianoRoll while the Note is still sounding
      while isSounding and endTimeSliceIndex < rasterLength:
         # does note sound in this time slice?
         if self._timeSliceContainsNote(endTimeSliceIndex, noteIndex):
            endTimeSliceIndex += 1   # yes, so advance to the next time slice
         else:
            isSounding = False   # no, we found the end of the note
      # now, endTimeSliceIndex points to the first time slice where the
      # note does not sound

      endTimeSliceIndex -= 1   # the note ended in the previous time slice

      return endTimeSliceIndex

   def timeSliceToString(self, pianoRollIndex):
      """
      Prints the contents of a timeslice into a string.

      param int pianoRollIndex: the index of the timeslice
      return str: a string with the time slice's data
      """
      s = ""
      timeSlice = self.getTimeSlice(pianoRollIndex)
      for index in range(len(timeSlice)):
         pitch = self.getNote(abs(timeSlice[index])).getPitch()
         s += str(pitch) + " "
      return s

   def getQuantizedVoice(self, voice):
      """
      Constructs and returns a part that is the representation of a certain assigned voice in the score from the pianoroll.
      This voice is the "quantized" voice, as it is represented in the pianoroll.

      param int voice: the voice to be represented as a part
      return Part: a Part representing the quantized voice of the score, empty part if voice doesn't exist
      """
      voicePart = Part(PIANO)   # to be the representation of the voice
      voicePhrase = Phrase(0.0) # start time 0.0
      voicePart.addPhrase(voicePhrase)

      currentTime = 0.0   # initialize time to 0.0
      prLength = self.getLength()   # length of the pianoRoll

      # Traverse the pianoRoll, looking at each timeSlice
      for rasterIndex in range(prLength):
         timeSlice = self.getTimeSlice(rasterIndex)

         # for each note in the timeSlice
         for timeSliceIndex in range(len(timeSlice)):
            # only look at notes that begin here
            if timeSlice[timeSliceIndex] > 0:
               # look at note
               currNote = self.getNote(timeSlice[timeSliceIndex])
               # get note's voice
               notesVoice = currNote.getVoice()

               # if note is in the voice we want
               if notesVoice == voice:
                  newNote = currNote.copy()   # get a copy so that we do not modify the original note
                  # set newNote's length to be the currNote's quantized duration (as represented in the piano roll)
                  newNote.setLength(currNote.getDurationQuantized())
                  newNote.setDuration(currNote.getDurationQuantized()) # Ensure duration is set too

                  voicePhrase.addNote(newNote)   # ...add note to phrase

         # increase the currentTime to reflect the next position in the pianoRoll
         currentTime += self.quantum

      return voicePart

   def getVoice(self, voice):
      """
      Constructs and returns a part that is the representation of a certain assigned voice in the score.
      This voice consists of notes from the note array, thus it is the "unquantized" voice as it appears in the
      original score.

      param int voice: the voice to be represented as a part
      return Part: a Part representing the voice of the score
      """
      voicePart = Part(PIANO)   # to be the representation of the voice
      voicePhrase = Phrase(0.0) # start time 0.0
      voicePart.addPhrase(voicePhrase)

      prLength = self.getLength()   # length of the pianoRoll

      # Traverse the pianoRoll, looking at each timeSlice
      for rasterIndex in range(prLength):
         timeSlice = self.getTimeSlice(rasterIndex)

         # for each note in the timeSlice
         for timeSliceIndex in range(len(timeSlice)):
            # only look at notes that begin here
            if timeSlice[timeSliceIndex] > 0:
               # look at note
               currNote = self.getNote(timeSlice[timeSliceIndex])
               # get note's voice
               notesVoice = currNote.getVoice()
               # get note's start time
               noteStartTime = currNote.getStartTime()

               # if note is in the voice we want
               if notesVoice == voice:
                  voicePhrase.addNote(currNote)   # ...add note to phrase

      return voicePart

   def getScore(self):
      """
      This method returns a new Score based on the PianoRoll representation.
      The returned Score conisists of one Part per voice.  Each Part consists
      of a single Phrase, which consists of all the Notes of the corresponding
      voice sorted by start time and with necessary Rests added to account for
      temporal gaps between Notes.

      Precondition: pianoRoll has been populated and voiced.

      return Score: a Score reconstructed from the PianoRoll
      """
      rasterLength = self.getLength()   # stores length of the pianoRoll

      parts = {}   # stores a Part (value) for each voice (key)
      score = Score()   # new score to be returned

      currentTime = 0.0   # Initialize time to 0.0

      # The voicing algorithm has a known problem, once in a while.  It cannot be helped.
      # So, when this problem occurs, we need to do something special.  This flag alerts us
      # that the problem has occured (see below for more details)
      noteOverlapBug = False

      # traverse the pianoRoll, looking at each timeSlice for new notes
      for rasterIndex in range(rasterLength):
         timeSlice = self.getTimeSlice(rasterIndex)   # get the current time slice

         # for each note in the timeSlice, check if it is a new note and if so
         # add it in the corresponding voice's Part
         for timeSliceIndex in range(len(timeSlice)):
            # if this is a new note (not a continuation)...
            if timeSlice[timeSliceIndex] > 0:
               note = self.getNote(timeSlice[timeSliceIndex])   # get this note
               note = ExtendedNote(note)   # create a copy so we do not modify the original

               voice = note.getVoice()   # get the note's voice (as determined by our heuristic voicing algorithm)

               # now, note is ready for insertion in the corresponding voice's Part

               # get this voice's Part (if any) from the dictionary
               part = parts.get(voice)

               # if no Part exists for this voice yet, create one and add it to the dictionary
               # (this Part should contain a single Phrase, starting at the current beat)
               if part is None:   # is this a new voice?
                  # create a new Part
                  part = Part("Voice: " + str(voice), PIANO)

                  part.addPhrase(Phrase(note.getStartTimeQuantized()))   # add the Phrase to the Part (starting on the current beat)
                  parts[voice] = part   # add new Part to the dictionary

               # Now, 'part' points to the Part holding this voice's (single) Phrase.
               # (Note: this Phrase may or may not be empty.)

               # phrase = part.getPhraseList()[0]      # get the only phrase in this part
               phrase = part.getPhraseList()[part.getSize() - 1]   # get the current phrase in this part by getting the last phrase in the part

               # get the previous note in this Part (if any)
               prevNote = None
               if phrase.getSize() > 0:
                  prevNote = phrase.getNote(phrase.getSize() - 1)   # get the previous note (if any)

               # Now, 'prevNote' is the previous note (if any), and 'note' is note to be added
               timeGap = 0.0   # it holds the time gap between the current note and the previous note (if any)
               if prevNote is not None:   # if there is a previous note...
                  # Let's see if we need to add a rest (Phrases are sequences of Notes without
                  # temporal gaps; so, if we have a temporal gap, we need to add a Rest.)
                  # Note start times and rhythm values are quantized already
                  # (in timeSlice * quantum intervals).

                  prevNoteEndTime = prevNote.getStartTime() + prevNote.getLength()   # length = performance time
                  timeGap = currentTime - prevNoteEndTime

                  # now let's build the appropriate Rest (if needed)
                  if timeGap >= self.quantum:
                     rest = Note(REST, timeGap)
                     phrase.addNote(rest)

                  # BUG:  The following exposes the note overlap bug...
                  if timeGap < 0:
                     noteOverlapBug = True   # remember that we have a problem

               # now, we have added a rest (if there was a time gap between the end of the
               # last note and the beginning of the current note).

               # set its start time and duration to their quantized counterparts
               if not noteOverlapBug:
                  note.setStartTime(note.getStartTimeQuantized())
                  note.setDuration(note.getDurationQuantized())
                  note.setLength(note.getDurationQuantized())
               else:   # note overlap bug
                  # We are here because we have two notes in the same voice that overlap (this is due to a documented feature
                  # of the voicing algorithm.  So, we create a new phrase for the overlapping note and any subsequent notes.
                  part.addPhrase(Phrase(note.getStartTimeQuantized()))   # add the Phrase to the Part (starting on the current beat)
                  phrase = part.getPhraseList()[part.getSize() - 1]   # get current phrase
                  noteOverlapBug = False   # reset

               # let's add the current note in the phrase -- addNote() will use Note's startTime and duration/rhythmValue
               # to create the new note.  Since these are now quantized, we will get the desired effect.
               phrase.addNote(note)

         # increase the currentTime to reflect the next position in the pianoRoll
         currentTime += self.quantum

      # Now, dictionary 'parts' contain one part for every distinct voice encountered
      # in the piano roll.  Each part contains a single phrase.  Each phrase contains
      # a sequence of notes with quantized start times and durations, and any needed rests
      # to account for temporal gaps between notes in the piano roll.

      # add Parts to score
      for part in parts.values():
         score.addPart(part)

      # Now, score contains all generated parts.

      # Let's finalize things, by setting score's other needed parameters
      score.setTimeSignature(self.numerator, self.denominator)
      score.setTempo(self.tempo)

      return score

   def getNScore(self):
      """
      Returns a score created from the individual (quantized) voices obtained from the pianoroll.

      return Score: score created from the pianoroll
      """
      score = Score()   # new score that will be returned

      # see how many voices this pianoroll has
      numVoices = self.getNumVoices()

      # add all the voices to the score
      for i in range(numVoices):
         score.addPart(self.getQuantizedVoice(i))

      # set score's values
      score.setTimeSignature(self.numerator, self.denominator)
      score.setTempo(self.tempo)

      if self.TEST_OUTPUT:
         print(score)

      return score

   def contigAndVoicePrintout(self, contigList):
      """
      This class is purely for testing purposes.  It outputs the data of the contigs made.

      param list[Contig] contigList: the list containing contigs created in the piano roll.
      """
      if not self.TEST_OUTPUT:
         return

      temp = None
      timeslice = []
      pitch = 0
      voice = 0
      note = None
      isvoiced = ""

      try:
         with open("PianoRoll-out.txt", "w") as out:
            out.write("Format:\ntimeslice (timeslice size)=(pitch,voice) (pitch,voice)\n\n")
            for i in range(len(contigList)):
               temp = contigList[i]

               isvoiced = "false"
               if temp.voiced:
                  isvoiced = "true"
               out.write("[New Contig] size: " + str(len(temp.voices)) + " capacity: " + str(len(temp.voices)) + " ")
               out.write("is voiced: " + isvoiced + "\n")

               for rollIndex in range(temp.start, temp.end + 1):
                  timeslice = self.getTimeSlice(rollIndex)
                  out.write("timeslice " + str(rollIndex) + " (" + str(len(timeslice)) + ")= ")
                  for sliceIndex in range(len(timeslice)):
                     note = self.getNote(abs(timeslice[sliceIndex]))
                     pitch = note.getPitch()
                     if sliceIndex < len(temp.voices):
                        voice = temp.voices[sliceIndex]
                        out.write("(" + str(pitch) + "," + str(voice) + ")  ")
                  out.write("\n")
      except Exception as e:
         print("Error: " + str(e))
