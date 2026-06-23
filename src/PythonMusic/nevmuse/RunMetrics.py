import os
import sys
import gc
from datetime import datetime

# add src to path if needed (though usually run from root with python -m nevmuse.RunMetrics)
srcDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import *
from .Surveyor import Surveyor
from .data.PianoRoll import PianoRoll
from .utilities.CSVWriter import CSVWriter

# import all simple metrics
from .metrics.simple import *


class RunMetrics:

   # determine the nevmuse directory (where this script lives)
   _scriptDir = os.path.dirname(os.path.abspath(__file__))

   # where to read MIDI files from, and write CSV file to (absolute paths)
   MIDIFolder = os.path.join(_scriptDir, "MIDI")
   scoreOutputFolder = os.path.join(MIDIFolder, "PianoRolled")
   CSVFolder = os.path.join(_scriptDir, "CSV")

   # 0.25 means that 1/16th is the shortest note duration to represent
   QUANTUM = 0.25

   @staticmethod
   def main():
      # generate datetime stamp for output filenames
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      csvFilename = os.path.join(RunMetrics.CSVFolder, f"metrics_{timestamp}.csv")

      metrics = [
         PitchMetric(2),
         PitchDistanceMetric(2),
         PitchDurationMetric(2),
         PitchDurationQuantizedMetric(2),

         ChromaticToneMetric(2),

         DurationMetric(2),
         DurationBigramMetric(2),
         DurationDistanceMetric(2),

         DurationQuantizedMetric(2),
         DurationQuantizedBigramMetric(2),
         DurationQuantizedDistanceMetric(2),

         ContourMelodyPitchMetric(2),
         ContourMelodyDurationMetric(2),
         ContourMelodyDurationQuantizedMetric(2),

         ContourBasslinePitchMetric(2),
         ContourBasslineDurationMetric(2),
         ContourBasslineDurationQuantizedMetric(2),

         MelodicIntervalMetric(2),
         MelodicBigramMetric(2),
         MelodicConsonanceMetric(2),

         HarmonicIntervalMetric(2),
         HarmonicBigramMetric(2),
         HarmonicConsonanceMetric(2),

         ChordMetric(2),
         ChordDensityMetric(2),
         ChordDistanceMetric(2),
         ChordNormalizedMetric(2),

         RestMetric(2)
      ]

      # ensure output directories exist
      for folder in [RunMetrics.scoreOutputFolder, RunMetrics.CSVFolder]:
         if not os.path.exists(folder):
            try:
               os.makedirs(folder)
            except OSError:
               pass   # ignore if exists

      # get MIDI files to process
      if not os.path.exists(RunMetrics.MIDIFolder):
         print(f"Directory {RunMetrics.MIDIFolder} does not exist.")
         return

      pieces = [f for f in os.listdir(RunMetrics.MIDIFolder) if f.lower().endswith(".mid")]

      if not pieces:
         print(f"The provided directory ({RunMetrics.MIDIFolder}) contains no useable files.")
         # in Python we normally don't throw exception for this in main script, just exit
         return

      print()
      print("-------------------------------------------------------------------------------")
      print(f"Start processing MIDI file batch in folder {RunMetrics.MIDIFolder}")
      print(f"Writing vectors in CSV file {csvFilename}")
      print()

      # process one MIDI file
      for piece in pieces:
         print(f"Opening {piece}...")

         # Read the midi file into the score
         # using standard Read.midi from music.py (which uses jMusic equivalent)
         score = Score()
         Read.midi(score, os.path.join(RunMetrics.MIDIFolder, piece))

         # extract metrics from score
         surveyor = Surveyor()

         # create PianoRoll and write reconstructed scores
         baseName = os.path.splitext(piece)[0]
         proll = PianoRoll(score, RunMetrics.QUANTUM)
         pscore = proll.getScore()
         pnscore = proll.getNScore()
         Write.midi(pscore, os.path.join(RunMetrics.scoreOutputFolder, f"{RunMetrics.QUANTUM}.getScore.{baseName}_{timestamp}.mid"))
         Write.midi(pnscore, os.path.join(RunMetrics.scoreOutputFolder, f"{RunMetrics.QUANTUM}.getNScore.{baseName}_{timestamp}.mid"))

         # and specify how much to quantize
         surveyor.survey(score, metrics, RunMetrics.QUANTUM)

         # write extracted metrics to CSV file
         print("appending vector to CSV file... ", end="")
         RunMetrics._outputMetric(metrics, piece, csvFilename)
         print("done.")
         print()

         # force garbage collection (less critical in Python but good for large batches)
         gc.collect()

      print("Done processing MIDI file batch.")

   @staticmethod
   def _outputMetric(metrics, MIDIFileName, logFileName):
      measurements = []

      for metric in metrics:
         measurements.append(metric.getMeasurement())

      CSVWriter.appendCSV(logFileName, MIDIFileName, measurements)


if __name__ == "__main__":
   RunMetrics.main()
