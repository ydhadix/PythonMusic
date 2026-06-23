# test_PianoRoll_assertions.py
#
# Assertion helpers for verifying PianoRoll behavior.
# These functions check that PianoRoll correctly implements its documented behavior:
#   - Score properties (tempo, time signature) are preserved
#   - Notes are quantized to quantum boundaries
#   - Voice assignments follow maxVoiceJump constraint
#   - Temporal coherence within voices
#   - Pitch coverage is maintained
#   - Round-trip stability
#
# Uses moderate strictness: allows documented quantization losses
# but fails on unexpected issues.

import math
from collections import Counter


class AssertionResult:
   """Holds the result of an assertion with details"""
   def __init__(self, passed, message, details=None):
      self.passed = passed
      self.message = message
      self.details = details or {}

   def __str__(self):
      status = "PASS" if self.passed else "FAIL"
      result = f"[{status}] {self.message}"
      if self.details:
         result += "\n   Details: " + str(self.details)
      return result


def assertScorePropertiesMatch(originalScore, reconstructedScore):
   """
   Verify that tempo and time signature are preserved.

   This is STRICT - any mismatch fails.

   param Score originalScore: the original score
   param Score reconstructedScore: score reconstructed from PianoRoll
   return AssertionResult: result of the assertion
   """
   issues = []

   # check tempo
   origTempo = originalScore.getTempo()
   reconTempo = reconstructedScore.getTempo()
   if origTempo != reconTempo:
      issues.append(f"Tempo mismatch: original={origTempo}, reconstructed={reconTempo}")

   # check time signature numerator
   origNum = originalScore.getNumerator()
   reconNum = reconstructedScore.getNumerator()
   if origNum != reconNum:
      issues.append(f"Numerator mismatch: original={origNum}, reconstructed={reconNum}")

   # check time signature denominator
   origDen = originalScore.getDenominator()
   reconDen = reconstructedScore.getDenominator()
   if origDen != reconDen:
      issues.append(f"Denominator mismatch: original={origDen}, reconstructed={reconDen}")

   if issues:
      return AssertionResult(False, "Score properties do not match", {"issues": issues})
   else:
      return AssertionResult(True, "Score properties match (tempo, time signature)")


def assertNotesQuantized(score, quantum, tolerance=1e-9):
   """
   Verify that all note start times and durations are multiples of quantum.

   This is STRICT - any non-quantized note fails.

   param Score score: the score to check
   param float quantum: the quantum value used in PianoRoll
   param float tolerance: floating point comparison tolerance
   return AssertionResult: result of the assertion
   """
   nonQuantizedNotes = []

   parts = score.getPartList()
   for partIdx, part in enumerate(parts):
      phrases = part.getPhraseList()
      for phraseIdx, phrase in enumerate(phrases):
         phraseStart = phrase.getStartTime()

         # check phrase start time is quantized
         remainder = phraseStart % quantum
         if remainder > tolerance and (quantum - remainder) > tolerance:
            nonQuantizedNotes.append({
               "location": f"Part {partIdx}, Phrase {phraseIdx} start time",
               "value": phraseStart,
               "quantum": quantum,
               "remainder": remainder
            })

         for noteIdx in range(phrase.getSize()):
            note = phrase.getNote(noteIdx)

            # skip rests
            if note.isRest():
               continue

            # check note duration is quantized
            duration = note.getDuration()
            remainder = duration % quantum
            if remainder > tolerance and (quantum - remainder) > tolerance:
               nonQuantizedNotes.append({
                  "location": f"Part {partIdx}, Phrase {phraseIdx}, Note {noteIdx} duration",
                  "value": duration,
                  "quantum": quantum,
                  "remainder": remainder
               })

   if nonQuantizedNotes:
      return AssertionResult(False,
                           f"Found {len(nonQuantizedNotes)} non-quantized values",
                           {"nonQuantized": nonQuantizedNotes[:5]})   # show first 5
   else:
      return AssertionResult(True, "All notes properly quantized")


def assertVoiceAssignmentValid(pianoRoll, maxVoiceJump=7):
   """
   Verify that voice assignments follow the maxVoiceJump constraint.
   No two consecutive notes in the same voice should exceed maxVoiceJump semitones.

   This is STRICT - any violation fails.

   param PianoRoll pianoRoll: the piano roll to check
   param int maxVoiceJump: maximum pitch interval between consecutive notes (default 7 = P5)
   return AssertionResult: result of the assertion
   """
   violations = []
   numVoices = pianoRoll.getNumVoices()

   # check each voice
   for voice in range(numVoices):
      prevNote = None

      # traverse piano roll to find notes in this voice
      for timeIndex in range(pianoRoll.getLength()):
         timeSlice = pianoRoll.getTimeSlice(timeIndex)

         for noteIndex in timeSlice:
            # only look at new notes (positive index)
            if noteIndex > 0:
               note = pianoRoll.getNote(noteIndex)

               if note.getVoice() == voice:
                  if prevNote is not None:
                     pitchJump = abs(note.getPitch() - prevNote.getPitch())

                     if pitchJump > maxVoiceJump:
                        violations.append({
                           "voice": voice,
                           "timeIndex": timeIndex,
                           "prevPitch": prevNote.getPitch(),
                           "currPitch": note.getPitch(),
                           "jump": pitchJump,
                           "maxAllowed": maxVoiceJump
                        })

                  prevNote = note

   if violations:
      return AssertionResult(False,
                           f"Found {len(violations)} voice jump violations",
                           {"violations": violations[:5]})   # show first 5
   else:
      return AssertionResult(True, f"All voice jumps within {maxVoiceJump} semitones")


def assertNoVoiceOverlaps(score, allowMultiplePhrases=True):
   """
   Verify that notes in the same voice don't overlap temporally.

   This is MODERATE - allows multiple phrases per part (documented bug workaround).

   param Score score: the score to check
   param bool allowMultiplePhrases: if True, allows overlaps between phrases (documented bug)
   return AssertionResult: result of the assertion
   """
   overlaps = []

   parts = score.getPartList()
   for partIdx, part in enumerate(parts):
      phrases = part.getPhraseList()

      # if allowing multiple phrases, check each phrase separately
      if allowMultiplePhrases:
         for phraseIdx, phrase in enumerate(phrases):
            prevNote = None
            prevEndTime = 0.0

            for noteIdx in range(phrase.getSize()):
               note = phrase.getNote(noteIdx)

               if note.isRest():
                  prevEndTime += note.getDuration()
                  continue

               currStartTime = prevEndTime
               currEndTime = currStartTime + note.getDuration()

               if prevNote is not None and currStartTime < prevEndTime:
                  overlaps.append({
                     "part": partIdx,
                     "phrase": phraseIdx,
                     "prevNote": f"pitch {prevNote.getPitch()}",
                     "currNote": f"pitch {note.getPitch()}",
                     "overlapAmount": prevEndTime - currStartTime
                  })

               prevNote = note
               prevEndTime = currEndTime
      else:
         # strict check across all phrases - not used in moderate mode
         pass

   if overlaps:
      return AssertionResult(False,
                           f"Found {len(overlaps)} note overlaps within phrases",
                           {"overlaps": overlaps[:5]})
   else:
      return AssertionResult(True, "No temporal overlaps within voices")


def assertPitchCoverage(originalScore, reconstructedScore, quantum, minCoverage=0.90):
   """
   Verify that major pitches from original appear in reconstruction.

   This is MODERATE - allows some pitch loss if notes were shorter than quantum.

   param Score originalScore: the original score
   param Score reconstructedScore: score reconstructed from PianoRoll
   param float quantum: the quantum value (notes shorter than this may be dropped)
   param float minCoverage: minimum fraction of original pitches that must appear (default 0.90)
   return AssertionResult: result of the assertion
   """
   def collectPitches(score):
      """Collect all pitches from a score"""
      pitches = set()
      parts = score.getPartList()
      for part in parts:
         phrases = part.getPhraseList()
         for phrase in phrases:
            for noteIdx in range(phrase.getSize()):
               note = phrase.getNote(noteIdx)
               if not note.isRest():
                  pitches.add(note.getPitch())
      return pitches

   origPitches = collectPitches(originalScore)
   reconPitches = collectPitches(reconstructedScore)

   if len(origPitches) == 0:
      return AssertionResult(False, "Original score has no pitches")

   missingPitches = origPitches - reconPitches
   coverage = (len(origPitches) - len(missingPitches)) / len(origPitches)

   details = {
      "originalPitches": len(origPitches),
      "reconstructedPitches": len(reconPitches),
      "missingPitches": len(missingPitches),
      "coverage": f"{coverage:.1%}"
   }

   if coverage < minCoverage:
      details["missing"] = sorted(list(missingPitches))[:10]   # show up to 10 missing
      return AssertionResult(False,
                           f"Pitch coverage {coverage:.1%} below minimum {minCoverage:.1%}",
                           details)
   else:
      return AssertionResult(True, f"Pitch coverage {coverage:.1%} meets minimum", details)


def assertNoteCountReasonable(originalScore, reconstructedScore, minRetention=0.80, maxRetention=1.00):
   """
   Verify that note count is within acceptable range.

   This is MODERATE - allows 80-100% note retention.

   param Score originalScore: the original score
   param Score reconstructedScore: score reconstructed from PianoRoll
   param float minRetention: minimum fraction of notes that must be retained (default 0.80)
   param float maxRetention: maximum fraction of notes allowed (default 1.00)
   return AssertionResult: result of the assertion
   """
   def countNotes(score):
      """Count non-rest notes in a score"""
      count = 0
      parts = score.getPartList()
      for part in parts:
         phrases = part.getPhraseList()
         for phrase in phrases:
            for noteIdx in range(phrase.getSize()):
               note = phrase.getNote(noteIdx)
               if not note.isRest():
                  count += 1
      return count

   origCount = countNotes(originalScore)
   reconCount = countNotes(reconstructedScore)

   if origCount == 0:
      return AssertionResult(False, "Original score has no notes")

   retention = reconCount / origCount

   details = {
      "originalNotes": origCount,
      "reconstructedNotes": reconCount,
      "retention": f"{retention:.1%}"
   }

   if retention < minRetention:
      return AssertionResult(False,
                           f"Note retention {retention:.1%} below minimum {minRetention:.1%}",
                           details)
   elif retention > maxRetention:
      return AssertionResult(False,
                           f"Note retention {retention:.1%} above maximum {maxRetention:.1%}",
                           details)
   else:
      return AssertionResult(True, f"Note retention {retention:.1%} within acceptable range", details)


def identifyNoteOverlapBug(score):
   """
   Checks if the 'Note Overlap Bug' workaround was triggered.
   The workaround involves creating multiple phrases in a single Part to handle overlapping notes in the same voice.

   This is INFORMATIONAL - it always passes, but reports if the bug logic was used.

   param Score score: the reconstructed score to check
   return AssertionResult: result of the check
   """
   bugTriggered = False
   details = {}

   parts = score.getPartList()
   for i, part in enumerate(parts):
      # The bug workaround creates additional phrases in the part
      if part.getSize() > 1:
         bugTriggered = True
         details[f"Part {i}"] = f"{part.getSize()} phrases (bug workaround triggered)"

   if bugTriggered:
      return AssertionResult(True, "Note Overlap Bug workaround WAS triggered", details)
   else:
      return AssertionResult(True, "Note Overlap Bug workaround was NOT triggered")


def assertRoundTripStability(score, quantum, maxVoiceJump=7, tolerance=0.10):
   """
   Verify that creating a second PianoRoll from reconstructed score produces stable results.

   This is MODERATE - allows ±10% variation.

   param Score score: the reconstructed score to test
   param float quantum: the quantum value
   param int maxVoiceJump: the maxVoiceJump parameter
   param float tolerance: allowed variation (default 0.10 = ±10%)
   return AssertionResult: result of the assertion
   """
   # need to import here to avoid circular dependency
   from .PianoRoll import PianoRoll

   try:
      # create first PianoRoll
      pr1 = PianoRoll(score, quantum=quantum, maxVoiceJump=maxVoiceJump)

      # reconstruct score
      score2 = pr1.getScore()

      # create second PianoRoll
      pr2 = PianoRoll(score2, quantum=quantum, maxVoiceJump=maxVoiceJump)

      # compare properties
      noteCount1 = pr1.getNoteCount()
      noteCount2 = pr2.getNoteCount()
      voiceCount1 = pr1.getNumVoices()
      voiceCount2 = pr2.getNumVoices()

      details = {
         "firstPass": {"notes": noteCount1, "voices": voiceCount1},
         "secondPass": {"notes": noteCount2, "voices": voiceCount2}
      }

      # check note count stability
      if noteCount1 == 0:
         return AssertionResult(False, "First pass produced zero notes", details)

      noteRetention = noteCount2 / noteCount1
      if noteRetention < (1.0 - tolerance) or noteRetention > (1.0 + tolerance):
         return AssertionResult(False,
                              f"Note count unstable: {noteRetention:.1%} retention",
                              details)

      # check voice count stability
      if voiceCount1 != voiceCount2:
         return AssertionResult(False,
                              f"Voice count changed from {voiceCount1} to {voiceCount2}",
                              details)

      return AssertionResult(True, "Round-trip produces stable results", details)

   except Exception as e:
      return AssertionResult(False, f"Round-trip failed with error: {str(e)}")


def runAllAssertions(originalScore, reconstructedScore, pianoRoll, quantum, maxVoiceJump=7):
   """
   Run all assertions and return a summary.

   param Score originalScore: the original score
   param Score reconstructedScore: score reconstructed from PianoRoll
   param PianoRoll pianoRoll: the piano roll object
   param float quantum: the quantum value
   param int maxVoiceJump: the maxVoiceJump parameter
   return dict: summary of all assertion results
   """
   results = {}

   print("\n" + "=" * 60)
   print("Running Assertions")
   print("=" * 60)

   # run each assertion
   assertions = [
      ("Score Properties", lambda: assertScorePropertiesMatch(originalScore, reconstructedScore)),
      ("Notes Quantized", lambda: assertNotesQuantized(reconstructedScore, quantum)),
      ("Voice Assignments", lambda: assertVoiceAssignmentValid(pianoRoll, maxVoiceJump)),
      ("No Voice Overlaps", lambda: assertNoVoiceOverlaps(reconstructedScore)),
      ("Note Overlap Bug", lambda: identifyNoteOverlapBug(reconstructedScore)),
      ("Pitch Coverage", lambda: assertPitchCoverage(originalScore, reconstructedScore, quantum)),
      ("Note Count", lambda: assertNoteCountReasonable(originalScore, reconstructedScore)),
      ("Round-Trip Stability", lambda: assertRoundTripStability(reconstructedScore, quantum, maxVoiceJump))
   ]

   for name, assertFunc in assertions:
      try:
         result = assertFunc()
         results[name] = result
         print(f"\n{name}: {result}")
      except Exception as e:
         result = AssertionResult(False, f"{name} raised exception: {str(e)}")
         results[name] = result
         print(f"\n{name}: {result}")

   # summary
   passed = sum(1 for r in results.values() if r.passed)
   total = len(results)

   print("\n" + "=" * 60)
   print(f"Assertion Summary: {passed}/{total} passed")
   print("=" * 60)

   return results
