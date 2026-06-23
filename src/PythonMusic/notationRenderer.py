###############################################################################
# notationRenderer.py       Version 1.0     13-Nov-2025
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
# 1.0   13-Nov-2025 (tr)   Initial implementation.
#
###############################################################################

import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import sys

# NOTE: Local, function-level imports are used in this module. This is a
# deliberate choice to break a circular dependency, as 'music.py' imports this
# module for its View.notate() functionality. Optional dependencies like
# 'verovio' are also imported locally where they are used.

### Constants ################################################################

_PITCH_CLASSES = ['C', 'C', 'D', 'D', 'E', 'F', 'F', 'G', 'G', 'A', 'A', 'B']
_ACCIDENTALS = [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]   # 0 = natural, 1 = sharp

_DURATION_TYPES = {   # duration in quarter notes -> MusicXML note type
   4.0: 'whole',
   3.0: 'half',      # dotted half
   2.0: 'half',
   1.5: 'quarter',   # dotted quarter
   1.0: 'quarter',
   0.75: 'eighth',   # dotted eighth
   0.5: 'eighth',
   0.375: '16th',    # dotted 16th
   0.25: '16th',
   0.125: '32nd',
}

_DIVISIONS_PER_QUARTER_NOTE = 4   # MusicXML timing precision

_DRUM_MAP = {
    # MIDI Pitch: (display_step, display_octave, notehead)
    # Bass Drums
    35: ('F', 4, 'normal'),
    36: ('F', 4, 'normal'),
    # Snares
    38: ('C', 5, 'normal'),
    40: ('C', 5, 'x'), # Rimshot
    # Toms
    41: ('D', 5, 'normal'), # High Tom
    43: ('B', 4, 'normal'), # Mid Tom
    45: ('A', 4, 'normal'), # Mid Tom
    47: ('G', 4, 'normal'), # Low Tom
    # Hi-Hats
    42: ('G', 5, 'x'), # Closed Hi-Hat
    44: ('F', 5, 'x'), # Pedal Hi-Hat
    46: ('G', 5, 'circle-x'), # Open Hi-Hat
    # Cymbals
    49: ('A', 5, 'x'), # Crash Cymbal
    57: ('A', 5, 'x'), # Crash Cymbal
    51: ('F', 5, 'x'), # Ride Cymbal
}


### API (called from music.py) ###############################################

def _showNotation(score, title="Sheet Music", writeToFile=False):
   """
   Renders a Score object into visual sheet music and displays it.

   This is the main public entry point for the notation rendering feature.
   It orchestrates the conversion of a PythonMusic Score into a MusicXML
   data structure, which is then rendered into an SVG image using the
   Verovio library. If Verovio is not installed, it saves the MusicXML
   file as a fallback, allowing users to open it in other notation software.

   Parameters:
      score (Score): The score object containing the musical data to render.
      title (str): The title for the sheet music, used for the window and filename.

   Returns:
      bool: True if rendering to SVG was successful, False otherwise.
   """
   # validate input
   if not hasattr(score, 'getPartList'):
      print("Error: Invalid score object")
      return False

   # determine output path for SVG file relative to the calling script
   try:
      # get the directory of the main script
      script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
   except (IndexError, AttributeError):
      # fallback for interactive sessions
      script_dir = os.getcwd()

   # output_dir = os.path.join(script_dir, "notation")

   # # create the notation directory if it doesn't exist
   # os.makedirs(output_dir, exist_ok=True)

   # Generate filename from title
   if title and title.strip() and title.strip() != "Untitled Score":
      filename_base = title.strip().replace(' ', '_')
      svg_filename = filename_base + ".svg"
   else:
      svg_filename = "sheet_music.svg"

   output_path = os.path.join(script_dir, svg_filename)

   # generate MusicXML
   musicxml = _scoreToMusicXML(score)

   # try to render with Verovio
   svg = _renderToSVG(musicxml)

   if svg is not None:
      # success - save file and open in viewer
      _openInViewer(svg, output_path, writeToFile)
      print(f"Sheet music saved to: {output_path}")
      return True
   else:
      # fallback path for when Verovio is not installed or fails
      filename = f"{title.replace(' ', '_')}.musicxml"
      _saveMusicXML(musicxml, filename)

      # inform the user how to view the fallback file
      print("\n" + "=" * 70)
      print("Sheet music saved as MusicXML")
      print("=" * 70)
      print(f"File: {filename}")
      print("\nTo view as sheet music, install Verovio:")
      print("   pip install verovio")
      print("\nOr open the MusicXML file in MuseScore, Finale, or Sibelius.")
      print("=" * 70 + "\n")

      return False


### MusicXML Generation ######################################################

def _calculateTotalMeasures(score):
   """
   Calculates the total number of measures needed for the score.

   This is based on the longest-running part, ensuring all parts
   in the MusicXML output have the same number of measures.

   Parameters:
      score (Score): The score to analyze.

   Returns:
      int: The total number of measures needed.
   """
   beatsPerMeasure = score.getNumerator()
   beatValue = score.getDenominator()
   measureDuration = beatsPerMeasure * (4.0 / beatValue)

   # find the end time of the longest part
   maxEndTime = 0.0
   for part in score.getPartList():
      if part.getPhraseList():
         partEndTime = part.getEndTime()
         maxEndTime = max(maxEndTime, partEndTime)

   # if score is empty, return at least 1 measure
   if maxEndTime == 0.0:
      return 1

   # calculate number of measures needed (round up)
   import math
   totalMeasures = math.ceil(maxEndTime / measureDuration)

   return totalMeasures


def _scoreToMusicXML(score):
   """
   Converts a PythonMusic Score object into a MusicXML string.

   This function builds the complete MusicXML document structure,
   including metadata, the part-list, and the musical data for each part.
   It serves as the central hub for assembling the final XML output.

   Parameters:
      score (Score): The score object to be converted.

   Returns:
      str: A string containing the complete MusicXML representation of the score.
   """
   from music import Part

   # create root element
   root = ET.Element('score-partwise')
   root.set('version', '4.0')

   # add metadata
   identification = ET.SubElement(root, 'identification')
   encoding = ET.SubElement(identification, 'encoding')
   software = ET.SubElement(encoding, 'software')
   software.text = 'PythonMusic'

   # create part list
   partList = ET.SubElement(root, 'part-list')

   parts = score.getPartList()
   if not parts:
      # if a score has no parts, create a default empty one to ensure a valid, renderable file

      parts = [Part()]

   # add each part to part list
   for i, part in enumerate(parts):
      partId = f'P{i+1}'
      scorePart = ET.SubElement(partList, 'score-part')
      scorePart.set('id', partId)

      partName = ET.SubElement(scorePart, 'part-name')
      partName.text = part.getTitle() if part.getTitle() else f"Part {i+1}"

      # for drum parts, specify the MIDI channel and program to ensure correct percussion rendering
      if part.getChannel() == 9:
         midi_instrument = ET.SubElement(scorePart, 'midi-instrument')
         midi_instrument.set('id', f'P{i+1}-I1')
         midi_channel = ET.SubElement(midi_instrument, 'midi-channel')
         midi_channel.text = '10'
         midi_program = ET.SubElement(midi_instrument, 'midi-program')
         midi_program.text = '1'  # General MIDI drum kit

   # calculate total number of measures needed (based on longest part)
   totalMeasures = _calculateTotalMeasures(score)

   # add each part's content
   for i, part in enumerate(parts):
      partId = f'P{i+1}'
      isDrumPart = (part.getChannel() == 9)
      _addPartToXML(root, part, partId, score, isDrumPart, totalMeasures)

   # convert to pretty-printed XML string
   xmlString = _prettifyXML(root)
   return xmlString


def _addPartToXML(root, part, partId, score, isDrumPart, totalMeasures):
   """
   Adds a single musical part's data to the MusicXML tree.

   This function processes all phrases within a given Part object,
   builds a timeline of notes, groups them into measures, and then
   delegates the creation of each measure's XML representation. It also
   determines the appropriate clef for the part based on its average pitch.

   Parameters:
      root (ET.Element): The root <score-partwise> XML element.
      part (Part): The Part object to add.
      partId (str): The unique identifier for this part (e.g., "P1").
      score (Score): The parent Score object, used for context like time signature.
      isDrumPart (bool): True if this part is for percussion, affecting clef and note representation.
      totalMeasures (int): The total number of measures in the score (all parts must have this many).
   """
   partElement = ET.SubElement(root, 'part')
   partElement.set('id', partId)

   # determine the appropriate clef for the part to improve readability
   if isDrumPart:
      clef_sign = 'percussion'   # use percussion clef for drum parts
      clef_line = None
   else:
      # for pitched instruments, choose a clef based on the average pitch
      average_pitch = _getAveragePitch(part)
      if average_pitch >= 60:  # C4 (middle C) or higher suggests a treble clef
         clef_sign = 'G'
         clef_line = '2'
      else:   # lower pitches are more readable in bass clef
         clef_sign = 'F'
         clef_line = '4'

   phrases = part.getPhraseList()
   if not phrases:
      # create empty measures for all measures in the score
      for measureNum in range(1, totalMeasures + 1):
         _createEmptyMeasure(partElement, measureNum, score)
      return

   # build timeline of notes
   noteTimeline = _buildNoteTimeline(phrases)

   # group into measures
   measures = _groupIntoMeasures(noteTimeline, score)

   # add each measure
   for measureNum in range(1, totalMeasures + 1):
      if measureNum <= len(measures):
         # this measure has notes
         measure = measures[measureNum - 1]
         _addMeasureToXML(partElement, measure, measureNum, score, measureNum == 1, isDrumPart, clef_sign, clef_line)
      else:
         # this measure is empty (pad to match total measure count)
         _createEmptyMeasure(partElement, measureNum, score)


def _addMeasureToXML(partElement, measure, measureNum, score, isFirstMeasure, isDrumPart, clef_sign, clef_line):
   """
   Adds a single measure's data to a part element in the MusicXML tree.

   For the first measure of a part, this function also adds critical
   attributes like time signature, key signature, and clef. It then
   iterates through the notes within the measure and delegates their
   creation to _addNoteToXML.

   Parameters:
      partElement (ET.Element): The <part> XML element to which this measure will be added.
      measure (dict): A dictionary containing the notes for this measure.
      measureNum (int): The number of the measure (1-indexed).
      score (Score): The parent Score object for accessing global attributes.
      isFirstMeasure (bool): True if this is the first measure, requiring attributes to be written.
      isDrumPart (bool): True if the part is for percussion.
      clef_sign (str): The sign of the clef (e.g., 'G', 'F', 'percussion').
      clef_line (str): The line number for the clef, if applicable.
   """
   from music import REST

   measureElement = ET.SubElement(partElement, 'measure')
   measureElement.set('number', str(measureNum))

   # attributes like key, time, and clef are only needed in the first measure
   # or when they change mid-score. this avoids redundant data.
   if isFirstMeasure:
      attributes = ET.SubElement(measureElement, 'attributes')

      # divisions (ticks per quarter note)
      divisions = ET.SubElement(attributes, 'divisions')
      divisions.text = str(_DIVISIONS_PER_QUARTER_NOTE)

      # key signature
      key = ET.SubElement(attributes, 'key')
      fifths = ET.SubElement(key, 'fifths')
      fifths.text = str(score.getKeySignature())

      # time signature
      time = ET.SubElement(attributes, 'time')
      beats = ET.SubElement(time, 'beats')
      beats.text = str(score.getNumerator())
      beatType = ET.SubElement(time, 'beat-type')
      beatType.text = str(score.getDenominator())

      # clef
      clef = ET.SubElement(attributes, 'clef')
      sign = ET.SubElement(clef, 'sign')
      sign.text = clef_sign
      if clef_line:
         line = ET.SubElement(clef, 'line')
         line.text = clef_line

   # add notes to measure
   if not measure['notes']:
      # add whole rest if measure is empty
      _addRestToXML(measureElement, _DIVISIONS_PER_QUARTER_NOTE * 4)
   else:
      currentTime = 0.0  # track current position in the measure
      lastNoteStartTime = -1.0  # track start time of the last note for chord detection

      for noteData in measure['notes']:
         # handle both formats: (relTime, note) or (relTime, note, tie, duration)
         if len(noteData) == 2:
            relativeTime, note = noteData
            tieType = None
            overrideDuration = None
         else:
            relativeTime, note, tieType, overrideDuration = noteData

         # check for chord (notes at same time don't advance currentTime)
         isChordNote = (relativeTime == lastNoteStartTime)

         # if not a chord and there's a gap, insert a rest to fill it
         if not isChordNote and relativeTime > currentTime:
            restDuration = relativeTime - currentTime
            restDurationInDivisions = int(restDuration * _DIVISIONS_PER_QUARTER_NOTE)
            if restDurationInDivisions > 0:
               _addRestToXML(measureElement, restDurationInDivisions)
            currentTime = relativeTime

         # add the note
         _addNoteToXML(measureElement, note, score, tieType, overrideDuration, isChordNote, isDrumPart)

         # advance current time (unless this is a chord note)
         if not isChordNote:
            noteDuration = overrideDuration if overrideDuration is not None else note.getDuration()
            currentTime += noteDuration

         lastNoteStartTime = relativeTime


def _addNoteToXML(measureElement, note, score, tieType=None, overrideDuration=None, isChordNote=False, isDrumPart=False):
   """
   Adds a single note's data to a measure element in the MusicXML tree.

   This function handles the detailed representation of a note, including
   whether it's a pitched note, a rest, or a drum hit. It also manages
   complex notations like chords (by adding a <chord/> tag) and ties for
   notes that cross barlines.

   Parameters:
      measureElement (ET.Element): The <measure> XML element.
      note (Note): The Note object to add.
      score (Score): The parent Score object.
      tieType (str, optional): Indicates if the note starts or stops a tie ('tie-start', 'tie-stop').
      overrideDuration (float, optional): Used when a note is split across a barline.
      isChordNote (bool): True if this note is part of a chord.
      isDrumPart (bool): True if the note is for a percussion instrument.
   """
   from music import REST

   noteElement = ET.SubElement(measureElement, 'note')

   # the <chord/> tag tells the renderer to stack this note with the previous one
   if isChordNote:
      chord = ET.SubElement(noteElement, 'chord')

   # check if it's a rest
   if note.getPitch() == REST:
      rest = ET.SubElement(noteElement, 'rest')
   elif isDrumPart:
      # Handle drum note
      midiPitch = note.getPitch()
      if midiPitch in _DRUM_MAP:
         display_step, display_octave, notehead_type = _DRUM_MAP[midiPitch]

         unpitched = ET.SubElement(noteElement, 'unpitched')
         display_step_elem = ET.SubElement(unpitched, 'display-step')
         display_step_elem.text = display_step
         display_octave_elem = ET.SubElement(unpitched, 'display-octave')
         display_octave_elem.text = str(display_octave)

         notehead = ET.SubElement(noteElement, 'notehead')
         notehead.text = notehead_type
      else:
         # fallback for unmapped drum sounds to prevent invalid "rest in chord" errors
         unpitched = ET.SubElement(noteElement, 'unpitched')
         display_step_elem = ET.SubElement(unpitched, 'display-step')
         display_step_elem.text = 'C'
         display_octave_elem = ET.SubElement(unpitched, 'display-octave')
         display_octave_elem.text = '5'

         notehead = ET.SubElement(noteElement, 'notehead')
         notehead.text = 'normal'

   else:
      # Handle pitched note
      pitch = ET.SubElement(noteElement, 'pitch')

      midiPitch = note.getPitch()
      octave = (midiPitch // 12) - 1
      pitchClass = midiPitch % 12

      step = ET.SubElement(pitch, 'step')
      step.text = _PITCH_CLASSES[pitchClass]

      # add accidental if needed
      if _ACCIDENTALS[pitchClass] == 1:
         alter = ET.SubElement(pitch, 'alter')
         alter.text = '1'

      octaveElem = ET.SubElement(pitch, 'octave')
      octaveElem.text = str(octave)

   # add duration (note: PythonMusic stores durations in quarter note units, not seconds)
   duration = ET.SubElement(noteElement, 'duration')

   # use override duration for notes split across a barline, otherwise use the note's own duration
   durationInQuarters = overrideDuration if overrideDuration is not None else note.getDuration()
   durationInDivisions = int(durationInQuarters * _DIVISIONS_PER_QUARTER_NOTE)

   # ensure minimum duration to prevent XML errors
   if durationInDivisions < 1:
      durationInDivisions = 1

   duration.text = str(durationInDivisions)

   # add note type (whole, half, quarter, etc.)
   noteType = ET.SubElement(noteElement, 'type')
   noteType.text = _getNoteType(durationInQuarters)

   # add tie notation if needed
   if tieType == 'tie-start':
      tie = ET.SubElement(noteElement, 'tie')
      tie.set('type', 'start')
      notations = ET.SubElement(noteElement, 'notations')
      tied = ET.SubElement(notations, 'tied')
      tied.set('type', 'start')
   elif tieType == 'tie-stop':
      tie = ET.SubElement(noteElement, 'tie')
      tie.set('type', 'stop')
      notations = ET.SubElement(noteElement, 'notations')
      tied = ET.SubElement(notations, 'tied')
      tied.set('type', 'stop')


def _addRestToXML(measureElement, duration):
   """
   Adds a rest element to a measure in the MusicXML tree.

   This is a helper function for creating a rest of a specific duration,
   typically used to fill empty measures or gaps between notes.

   Parameters:
      measureElement (ET.Element): The <measure> XML element.
      duration (int): The duration of the rest in MusicXML divisions.
   """
   noteElement = ET.SubElement(measureElement, 'note')
   rest = ET.SubElement(noteElement, 'rest')
   durationElem = ET.SubElement(noteElement, 'duration')
   durationElem.text = str(duration)

   # determine the appropriate note type for the rest duration
   durationInQuarters = duration / _DIVISIONS_PER_QUARTER_NOTE
   noteType = ET.SubElement(noteElement, 'type')
   noteType.text = _getNoteType(durationInQuarters)


def _createEmptyMeasure(partElement, measureNum, score):
   """
   Creates a complete, empty measure containing a whole rest.

   This is used when a part contains no notes or has significant gaps,
   ensuring the MusicXML structure remains valid and visually coherent.

   Parameters:
      partElement (ET.Element): The <part> XML element.
      measureNum (int): The measure number to create.
      score (Score): The parent Score object for context.
   """
   measureElement = ET.SubElement(partElement, 'measure')
   measureElement.set('number', str(measureNum))

   # add attributes
   attributes = ET.SubElement(measureElement, 'attributes')
   divisions = ET.SubElement(attributes, 'divisions')
   divisions.text = str(_DIVISIONS_PER_QUARTER_NOTE)

   key = ET.SubElement(attributes, 'key')
   fifths = ET.SubElement(key, 'fifths')
   fifths.text = '0'

   time = ET.SubElement(attributes, 'time')
   beats = ET.SubElement(time, 'beats')
   beats.text = str(score.getNumerator())
   beatType = ET.SubElement(time, 'beat-type')
   beatType.text = str(score.getDenominator())

   clef = ET.SubElement(attributes, 'clef')
   sign = ET.SubElement(clef, 'sign')
   sign.text = 'G'
   line = ET.SubElement(clef, 'line')
   line.text = '2'

   # add whole rest
   _addRestToXML(measureElement, _DIVISIONS_PER_QUARTER_NOTE * 4)


### Timeline & Measure Processing ############################################

def _buildNoteTimeline(phrases):
   """
   Builds a linear, time-sorted timeline of notes from a list of phrases.

   This function is crucial for converting the hierarchical Phrase/Note data
   structure into a flat list that can be easily processed into measures.
   A key responsibility is to correct the durations of notes within chords.
   In the source data, only the last note of a chord might have the correct
   duration, while others are zero. This function ensures all notes in a
   chord share the same, correct duration for proper notation.

   Parameters:
      phrases (list): A list of Phrase objects to process.

   Returns:
      list: A list of (startTime, Note) tuples, sorted by start time.
   """
   timeline = []

   for phrase in phrases:
      # get phrase start time in quarter notes
      phraseStartTime = phrase.getStartTime() if phrase.getStartTime() is not None else 0.0

      # process each note in the phrase
      for noteIndex in range(phrase.getSize()):
         note = phrase.getNote(noteIndex)

         # get note start time relative to phrase start (in quarter notes)
         noteStartTime = phrase.getNoteStartTime(noteIndex)

         # calculate absolute start time
         absoluteStartTime = phraseStartTime + noteStartTime

         timeline.append((absoluteStartTime, note))

   # sort by start time to ensure chronological processing
   timeline.sort(key=lambda x: x[0])

   # post-process the timeline to fix chord durations for accurate notation
   fixed_timeline = []
   i = 0
   while i < len(timeline):
      current_start_time, current_note = timeline[i]

      # check for a chord by looking ahead for notes with the same start time
      if i + 1 < len(timeline) and timeline[i+1][0] == current_start_time:
         chord_notes_group = [(current_start_time, current_note)]
         j = i + 1
         # gather all notes that belong to the same chord
         while j < len(timeline) and timeline[j][0] == current_start_time:
            chord_notes_group.append(timeline[j])
            j += 1

         # find the actual duration from the last note of the chord, which holds the value
         chord_duration = 0
         for _, note in reversed(chord_notes_group):
            if note.getDuration() > 0:
               chord_duration = note.getDuration()
               break

         # as a fallback, use the last note's duration even if it's zero
         if chord_duration == 0:
             chord_duration = chord_notes_group[-1][1].getDuration()

         # create new note objects with the corrected duration to avoid side effects
         for start_time, old_note in chord_notes_group:
            new_note = old_note.copy()
            new_note.setDuration(chord_duration)
            fixed_timeline.append((start_time, new_note))

         i = j  # move index past the just-processed chord notes
      else:
         # a single note, not part of a chord, so add it directly
         fixed_timeline.append((current_start_time, current_note))
         i += 1

   return fixed_timeline


def _groupIntoMeasures(noteTimeline, score):
   """
   Groups a flat timeline of notes into measures based on the time signature.

   This function is responsible for the complex logic of fitting notes into
   the temporal boundaries of measures. It is chord-aware, processing
   notes that start at the same time as a single unit. Its most critical
   task is to correctly split notes or chords that cross a barline, creating
   tied notes in the process to ensure musical continuity.

   Parameters:
      noteTimeline (list): A sorted list of (startTime, Note) tuples.
      score (Score): The parent Score object, needed for time signature context.

   Returns:
      list: A list of measure dictionaries, where each dictionary contains
            the notes belonging to that measure.
   """
   from music import REST # local import to avoid circular dependency
   measures = []
   beatsPerMeasure = score.getNumerator()
   beatValue = score.getDenominator()
   measureDuration = beatsPerMeasure * (4.0 / beatValue)

   if not noteTimeline:
      return [{'notes': [], 'startTime': 0.0}]

   measureStartTime = 0.0
   currentMeasure = {'notes': [], 'startTime': 0.0}

   timeline_idx = 0
   while timeline_idx < len(noteTimeline):
      # step 1. group notes starting at the same time (chords)
      startTime, first_note_in_group = noteTimeline[timeline_idx]

      note_group = [first_note_in_group]
      next_idx = timeline_idx + 1
      while next_idx < len(noteTimeline) and noteTimeline[next_idx][0] == startTime:
         note_group.append(noteTimeline[next_idx][1])
         next_idx += 1

      # if a chord contains both notes and rests, remove the rests to prevent invalid xml
      has_real_notes = any(n.getPitch() != REST for n in note_group)
      if has_real_notes and len(note_group) > 1:
         note_group = [n for n in note_group if n.getPitch() != REST]

      # the duration of the group is determined by its constituent notes (which are now uniform)
      group_duration = note_group[0].getDuration()
      noteEndTime = startTime + group_duration

      # step 2. check if we need new empty measures before this group
      while startTime >= measureStartTime + measureDuration:
         # always append the current measure (whether it has notes or is empty)
         measures.append(currentMeasure)

         measureStartTime += measureDuration
         currentMeasure = {'notes': [], 'startTime': measureStartTime}

      # step 3: process the note/chord group, splitting it if it crosses a barline
      measureEndTime = measureStartTime + measureDuration
      relativeTime = startTime - measureStartTime

      if noteEndTime > measureEndTime:
         # the group crosses a barline, so it must be split into two tied notes
         durationInCurrentMeasure = measureEndTime - startTime
         remainingDuration = noteEndTime - measureEndTime

         # add the first part of the note/chord to the current measure
         if durationInCurrentMeasure > 0:
            for note in note_group:
               currentMeasure['notes'].append((relativeTime, note, 'tie-start', durationInCurrentMeasure))

         # finish the current measure and start the next one
         measures.append(currentMeasure)
         measureStartTime = measureEndTime
         currentMeasure = {'notes': [], 'startTime': measureStartTime}

         # add the remainder of the note/chord to the new measure
         if remainingDuration > 0:
            for note in note_group:
               currentMeasure['notes'].append((0.0, note, 'tie-stop', remainingDuration))
      else:
         # group fits entirely in the current measure
         for note in note_group:
            currentMeasure['notes'].append((relativeTime, note))

      # step 4: advance the timeline index past the notes just processed
      timeline_idx = next_idx

   # Add the last measure if it has notes
   if currentMeasure['notes']:
      measures.append(currentMeasure)

   # print(f"[_notationRenderer.py] Grouped measures (chord-aware): {measures}")
   return measures


### Rendering ################################################################

def _renderToSVG(musicxml):
   """
   Renders a MusicXML string into an SVG image using the Verovio library.

   This function acts as a wrapper around the Verovio toolkit. If Verovio
   is not installed, this function will fail gracefully by returning None,
   allowing the calling code to handle the fallback (e.g., by saving the
   raw MusicXML file).

   Parameters:
      musicxml (str): The MusicXML data to be rendered.

   Returns:
      str: A string containing the SVG data, or None if Verovio is not available.
   """
   try:
      import verovio
   except ImportError:
      return None   # verovio not available

   # create toolkit
   tk = verovio.toolkit(False)

   # ensure verovio fonts are available
   tk.setResourcePath(os.path.join(os.path.dirname(verovio.__file__), "data"))

   # configure options for the svg output, controlling layout and appearance
   tk.setOptions({
      'pageWidth': 2100,
      'pageHeight': 2970,
      'scale': 60,
      'adjustPageHeight': True   # ensures the svg fits the content vertically
   })

   # load MusicXML
   tk.loadData(musicxml)

   # render to SVG
   svg = tk.renderToSVG(1)   # render page 1

   return svg


def _openInViewer(svg, path, writeToFile):
   """
   Saves an SVG string to a file and opens it with the default system viewer.

   This provides a cross-platform way to immediately display the generated
   sheet music to the user in whatever application they have associated
   with SVG files (e.g., a web browser, image viewer).

   Parameters:
      svg (str): The SVG data to save and display.
      path (str): The absolute file path to save the SVG to.
   """
   import pathlib, webbrowser, tempfile, urllib.parse

   if writeToFile:
      # save to specified path
      with open(path, 'w', encoding='utf-8') as f:
         f.write(svg)
         svgPath = pathlib.Path(path).expanduser().resolve()  # absolute path to written SVG

   else:
      # save to temporary location
      with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as f:
         f.write(svg)
         svgPath = pathlib.Path(f.name).resolve()  # absolute path to temporary SVG

   if svgPath.is_file():
      svgURL = svgPath.as_uri()  # convert filepath to URL (with correct space handling)

      # generate minimal HTML wrapper
      # SVG is a generic document type, so often get opened in text editors
      # (TextMate, VSCode, etc.).  We want to open the SVG in the user's
      # default web browser, so we wrap it in HTML before opening.
      html = f"""<!doctype html>
      <html>
      <head>
         <meta charset="utf-8">
         <meta name="viewport" content="width=device-width, initial-scale=1">
         <title>{svgPath.name}</title>
         <style>
            html, body {{ height: 100%; margin: 0; }}
            body {{ display: grid; place-items: center; background: #fff; }}
            img {{ max-width: 100vw; max-height: 100vh; }}
         </style>
      </head>
      <body>
         <img src="{svgURL}" alt="{svgPath.name}">
      </body>
      </html>
      """

      # write wrapper to a temporary file
      with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
         f.write(html)
         htmlPath = pathlib.Path(f.name).resolve()  # absolute path to HTML
         htmlURL = htmlPath.as_uri()  # convert to URL

      ok = webbrowser.open(htmlURL, new=2)  # open in new tab, if possible
      if not ok:
         webbrowser.open(htmlURL)  # fallback to new browser window

   else:
      print(f"View.notate(): Couldn't open generated SVG '{path}' (You can open this notation in most web browsers).")

   # # use the appropriate system command to open the file in the default viewer
   # if sys.platform == 'win32':
   #    os.startfile(path)
   # elif sys.platform == 'darwin':   # macOS
   #    subprocess.run(['open', path])
   # else:   # linux
   #    subprocess.run(['xdg-open', path])


def _saveMusicXML(musicxml, filename):
   """
   Saves the MusicXML string to a file.

   This function is used as a fallback when direct SVG rendering is not
   available (i.e., Verovio is not installed). This allows the user to
   open the generated .musicxml file in an external notation program.

   Parameters:
      musicxml (str): The MusicXML data to save.
      filename (str): The name of the file to save the data to.
   """
   with open(filename, 'w', encoding='utf-8') as f:
      f.write(musicxml)

   print(f"MusicXML saved: {filename}")


### Utility Functions ########################################################

def _getAveragePitch(part):
   """
   Calculates the average MIDI pitch for all notes in a part.

   This is used to make an educated guess about which clef (e.g., treble
   vs. bass) is most appropriate for rendering the part's notation.

   Parameters:
      part (Part): The Part object to analyze.

   Returns:
      float: The average MIDI pitch, or a default of 60.0 (C4) if the part is empty.
   """
   from music import REST
   pitches = []
   for phrase in part.getPhraseList():
      for note in phrase.getNoteList():
         pitch = note.getPitch()
         if pitch != REST:
            pitches.append(pitch)

   if not pitches:
      return 60.0  # Default to C4 if no pitched notes

   return sum(pitches) / len(pitches)


def _getNoteType(durationInQuarters):
   """
   Maps a duration to the nearest standard MusicXML note type string.

   This function translates a numeric duration (in terms of quarter notes)
   into the symbolic representation required by MusicXML, such as 'whole',
   'half', or 'quarter'. It finds the closest standard type to handle
   both exact and irregular durations.

   Parameters:
      durationInQuarters (float): The note's duration in quarter notes.

   Returns:
      str: The corresponding MusicXML note type (e.g., 'quarter').
   """
   # find closest match
   closestType = 'quarter'
   minDiff = float('inf')

   for duration, noteType in _DURATION_TYPES.items():
      diff = abs(durationInQuarters - duration)
      if diff < minDiff:
         minDiff = diff
         closestType = noteType

   return closestType


def _prettifyXML(element):
   """
   Converts an XML element into a well-formatted, human-readable string.

   This utility takes the raw, unformatted XML generated by ElementTree and
   uses `minidom` to apply indentation. It also prepends the standard XML
   declaration and MusicXML DOCTYPE, making the output a valid and
   readable MusicXML file.

   Parameters:
      element (ET.Element): The root XML element to format.

   Returns:
      str: A pretty-printed XML string.
   """
   # ElementTree is fast for building but lacks a pretty-print feature.
   # so, we re-parse the string with minidom to get nice indentation.
   roughString = ET.tostring(element, encoding='unicode')
   reparsed = minidom.parseString(roughString)

   # add the required XML declaration and DOCTYPE for a valid MusicXML 4.0 file
   xmlDeclaration = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
   doctype = '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">\n'

   prettyXML = reparsed.toprettyxml(indent='   ')

   # minidom's toprettyxml adds its own xml declaration, which we need to remove
   # before adding our custom one with the correct doctype.
   lines = prettyXML.split('\n')
   prettyXML = '\n'.join(lines[1:])

   return xmlDeclaration + doctype + prettyXML
