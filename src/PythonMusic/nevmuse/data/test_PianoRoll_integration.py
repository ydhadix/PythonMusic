# test_PianoRoll_integration.py
#
# Integration test for PianoRoll that mirrors the original Java PianoRollVoiceTest.java
# and TestPianoRoll.py behavior.
#
# This test:
#   1. Reads MIDI files from an input folder
#   2. Creates PianoRolls with various quantum values
#   3. Reconstructs the Score using getScore() and getNScore()
#   4. Writes the reconstructed MIDI files to an output folder
#   5. Logs results for manual comparison
#
# Usage:
#   python -i test_PianoRoll_integration.py
#
# Or with custom folders:
#   python -i test_PianoRoll_integration.py <input_folder> <output_folder>

import os
import sys
from datetime import datetime

# add the src directory to the path so we can import our modules
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import Score, Read, Write
from .PianoRoll import PianoRoll
from .test_PianoRoll_assertions import runAllAssertions


def testOne(inputFolder, filename, outputFolder, quantum=0.25, timestamp=""):
   """
   Create a PianoRoll from a MIDI file and write the reconstructed score.

   This mirrors the Java TestOne() method from PianoRollVoiceTest.java.

   :param str inputFolder: folder containing input MIDI files
   :param str filename: name of the MIDI file to process
   :param str outputFolder: folder to write output MIDI files
   :param float quantum: time slice duration (default 0.25 = sixteenth note)
   :param str timestamp: datetime stamp for output filenames
   """
   inputPath = os.path.join(inputFolder, filename)

   print("\n" + "=" * 60)
   print(">>>>>>>> Reading " + filename)
   print("=" * 60)

   try:
      # read the MIDI file
      score = Score()
      Read.midi(score, inputPath)

      print("  Score tempo: " + str(score.getTempo()))
      print("  Score end time: " + str(score.getEndTime()))
      print("  Score time signature: " + str(score.getNumerator()) + "/" + str(score.getDenominator()))

      # create the PianoRoll
      print("\n  Creating PianoRoll with quantum=" + str(quantum) + "...")
      roll = PianoRoll(score, quantum=quantum)

      print("  PianoRoll created:")
      print("    Note count: " + str(roll.getNoteCount()))
      print("    Number of voices: " + str(roll.getNumVoices()))
      print("    Number of time slices: " + str(roll.getLength()))
      print("    Quantum: " + str(roll.getQuantum()))

      # reconstruct the score using getScore()
      print("\n  Reconstructing score with getScore()...")
      reconstructedScore = roll.getScore()

      # run assertions
      runAllAssertions(score, reconstructedScore, roll, quantum)

      # write the reconstructed MIDI file
      baseName = os.path.splitext(filename)[0]
      outputFilename = f"{quantum}.getScore.{baseName}_{timestamp}.mid"
      outputPath = os.path.join(outputFolder, outputFilename)
      Write.midi(reconstructedScore, outputPath)
      print("  Wrote: " + outputFilename)

      # also try getNScore() for comparison
      print("\n  Reconstructing score with getNScore()...")
      nScore = roll.getNScore()

      outputFilename2 = f"{quantum}.getNScore.{baseName}_{timestamp}.mid"
      outputPath2 = os.path.join(outputFolder, outputFilename2)
      Write.midi(nScore, outputPath2)
      print("  Wrote: " + outputFilename2)

      print("\n<<<<<<<< Done with " + filename)
      return True

   except Exception as e:
      print("\n@@@@@@@@ Problem with MIDI file \"" + filename + "\"")
      print("  Error: " + str(e))
      import traceback
      traceback.print_exc()
      return False


def runTests(inputFolder, outputFolder, quantumValues=None):
   """
   Run PianoRoll tests on all MIDI files in the input folder.

   :param str inputFolder: folder containing input MIDI files
   :param str outputFolder: folder to write output MIDI files
   :param list quantumValues: list of quantum values to test (default [0.25, 0.5, 1.0, 2.0])
   """
   if quantumValues is None:
      quantumValues = [0.25, 0.5, 1.0, 2.0]   # Updated default set

   # generate datetime stamp for output filenames
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

   # ensure output folder exists
   if not os.path.exists(outputFolder):
      os.makedirs(outputFolder)
      print("Created output folder: " + outputFolder)

   # get all MIDI files in the input folder
   midiFiles = [f for f in os.listdir(inputFolder) if f.lower().endswith(".mid")]

   if len(midiFiles) == 0:
      print("No MIDI files found in " + inputFolder)
      return

   print("\n" + "#" * 60)
   print("# PianoRoll Integration Test")
   print("# Input folder: " + inputFolder)
   print("# Output folder: " + outputFolder)
   print("# MIDI files found: " + str(len(midiFiles)))
   print("# Quantum values: " + str(quantumValues))
   print("# Timestamp: " + timestamp)
   print("#" * 60)

   # process each MIDI file
   results = []
   for filename in midiFiles:
      for quantum in quantumValues:
         success = testOne(inputFolder, filename, outputFolder, quantum, timestamp)
         results.append((filename, quantum, success))

   # print summary
   print("\n" + "=" * 60)
   print("SUMMARY")
   print("=" * 60)
   successes = sum(1 for r in results if r[2])
   failures = sum(1 for r in results if not r[2])
   print("  Total tests: " + str(len(results)))
   print("  Successes: " + str(successes))
   print("  Failures: " + str(failures))

   if failures > 0:
      print("\n  Failed tests:")
      for filename, quantum, success in results:
         if not success:
            print("    - " + filename + " (quantum=" + str(quantum) + ")")


def main():
   """
   Main entry point for the integration test.
   """
   # determine the nevmuse directory (parent of data folder)
   scriptDir = os.path.dirname(os.path.abspath(__file__))
   nevmuseDir = os.path.dirname(scriptDir)

   # default input and output folders
   if len(sys.argv) >= 3:
      inputFolder = sys.argv[1]
      outputFolder = sys.argv[2]
   else:
      # read from MIDI folder, write to MIDI/PianoRolled folder
      inputFolder = os.path.join(nevmuseDir, "MIDI")
      outputFolder = os.path.join(nevmuseDir, "MIDI", "PianoRolled")

   # quantum values to test
   # we test sixteenth note (0.25) up to half note (2.0)
   quantumValues = [0.25, 0.5, 1.0, 2.0]

   runTests(inputFolder, outputFolder, quantumValues)


# run the tests when executed directly
if __name__ == "__main__":
   main()
