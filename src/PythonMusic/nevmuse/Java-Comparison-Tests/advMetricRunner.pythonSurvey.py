#######################################################################################################
# advMetricRunner.jythonSurvey.py       Version 1.1     20-Sep-2025     Jimmy Cyganek, David Johnson, John Emerson,
#                                                          Luca Pellicoro, Patrick Roos, Bill Manaris
#######################################################################################################

### Description: Runs metrics on a folder of MIDI files, these metrics are saved into a CSV file

### 1.1 (Sep. 20, 2025) - Removed DurationDistanceMetric from Surveyor, as it returns innacurate measurements

# import libraries
import os
import sys
import unicodedata

# add src to path if needed
srcDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if srcDir not in sys.path:
   sys.path.insert(0, srcDir)

from music import *
from ..Surveyor import Surveyor
from ..metrics.simple import *   # import simple metrics


#####
# set MIDI file path
midiFolderPath = "Bach AoF Fugues"

# using os module, find everything in folder that ends in ".mid"
folderFileNames = os.listdir(midiFolderPath)   # get filenames in folder (as strings)


#####
# keep only MIDI files
midiFileNames = []
for name in folderFileNames:   # iterate through all filenames

   if name[-4:] == ".mid":     # is it a MIDI file?
      midiFileNames.append(name)   # yes, so remember it

# now, midiFileNames contains all the names of MIDI files in midiFolderPath


#####
# define metrics to apply (we only need to create them once - they will be reused for every MIDI file)
metrics = [
   PitchMetric(2),
#   PitchDistanceMetric(2),
   PitchDurationMetric(2),
   PitchDurationQuantizedMetric(2),            # added Jan. 6 2010

   ChromaticToneMetric(2),

   DurationMetric(2),
   DurationBigramMetric(2),
#   DurationDistanceMetric(2),                  # added Sep. 30 2009

   DurationQuantizedMetric(2),                 # added Jan. 6 2010
   DurationQuantizedBigramMetric(2),           # added Jan. 7 2010
   DurationQuantizedDistanceMetric(2),         # added Jan. 6 2010

   ContourMelodyPitchMetric(2),                # added Jan. 7 2010
   ContourMelodyDurationMetric(2),             # added Jan. 7 2010
   ContourMelodyDurationQuantizedMetric(2),    # added Jan. 7 2010

   ContourBasslinePitchMetric(2),              # added Jan. 7 2010
   ContourBasslineDurationMetric(2),           # added Jan. 7 2010
   ContourBasslineDurationQuantizedMetric(2),  # added Jan. 7 2010

   MelodicIntervalMetric(2),
   MelodicBigramMetric(2),
   MelodicConsonanceMetric(2),

   HarmonicIntervalMetric(2),
   HarmonicBigramMetric(2),
   HarmonicConsonanceMetric(2),

   ChordMetric(2),
   RestMetric(2)
]


#####
# function to return metrics for a MIDI file
def runMetrics(midiFilePath):

   # load MIDI into  Score object
   score = Score("Metric Score")
   Read.midi(score, midiFilePath)

   # initialize Surveyor and apply metrics to the score
   quantum = 0.25
   surveyor = Surveyor()
   surveyor.survey(score, metrics, quantum)

   # get measurements for each metric
   measurements = []
   for metric in metrics:   # iterate through each metric

      # get measurement
      measurement = metric.getMeasurement()
      measurements.append(measurement)

   #print measurements
   return measurements

#####
# create a unique identifier for each piece - used as an attribute in Weka!!!
index = 0   # initialize

# function to create CSV file using list of measurements
def writeCSVFile(measurements, midiFolderPath, midiFileName, csvfile):

   global index           # used for index Weka attribute

   index = index + 1      # create unique identifier for this piece

   csvfile.write("\n")    # move down a row

   # for each metric, get each measurement and add it to the corresponding column
   for measurement in measurements:

      values = measurement.valuesToArray()   # get attribute values for each metric

      # get value of each measurement and write it to CSV file
      for value in values:

         csvfile.write(convertToASCII(value) + ",")   # write it!!

   csvfile.write(convertToASCII(index) + ",")      # write index value to index column

   # Caution: remove comma from filename - if any (since CSV files use comma as delimiter)
   noCommaFileName = midiFileName.replace(",", "")

   # write filename to the filename column (last column)
   csvfile.write(convertToASCII(noCommaFileName))

   # ***
   print("Wrote row for", midiFileName)

#####
# function to remove non-ASCII characters
def convertToASCII(string):

   # ***
   #try:
   # convert input to unicode string (in Python 3, str is already unicode)
   unicodeString = str(string)

   # convert string to NFKD format (separate characters from accents - creates two characters from one)
   nfkdString = unicodedata.normalize('NFKD', unicodeString)

   # re-encode to ASCII - ignore non-ASCII characters (like accents or symbols)
   asciiBytes = nfkdString.encode('ascii', 'ignore')

   # decode back to string (Python 3 returns bytes from encode)
   asciiString = asciiBytes.decode('ascii')

   # return ASCII-only version of the string
   return asciiString

   #except:  # ***

      # if there is no error, return as a string
      #return str(string)


##### Main #####

# Goal: process all MIDI files, get their metrics, then put them into CSV file
# How I plan to do this:
# - Run runMetrics on the first item in midiFileNames
#   - This will return it's metrics
# - Create the first row of the CSV (metric measurement names, will become attribute names in Weka) of this first item
# - Then, run a for loop for every item in midiFileNames, take it's values, and add them as a new row to the CSV


#####

# output metrics headers, by running metrics on first MIDI file

# create file path to the first MIDI file (midiFileNames[0])
midiFilePath = os.path.join(midiFolderPath, midiFileNames[0])

# run runMetrics on the first item in midiFileNames
measurements = runMetrics(midiFilePath)

# open CSV file for output
with open(midiFolderPath + "_metrics.csv", mode="w") as csvfile:

   # output headers for all measurements to CSV file
   for measurement in measurements:

      keys = measurement.keysToArray()   # get attribute names for each metric

      # output headers for this measurement
      for key in keys:
         csvfile.write(key+",")          # write them in CSV file - comma used to separate columns

   # add final headers
   csvfile.write("Index,")     # write index attribute header
   csvfile.write("Filename")   # write filename attribute header

   # run metrics for each MIDI file, and store results in CSV file
   for midiFileName in midiFileNames:

      # create path to MIDI file
      midiFilePath = os.path.join(midiFolderPath, midiFileName)

      # calculate metrics for this MIDI file
      measurements = runMetrics(midiFilePath)

      # write results to CSV file
      writeCSVFile(measurements, midiFolderPath, midiFileName, csvfile)

# now, all metrics for all MIDI files have been written to CSV file

   # ***
   # Is this needed???
   # remember to close CSV file!!!
   #csvfile.close()

# ***
print(midiFolderPath + "_metrics.csv written.")
