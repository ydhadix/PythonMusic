import os
import csv
from ..data.Measurement import Measurement

class CSVWriter:
   """
   This class contains static methods for writing Measurement values to CSV files.

   author Luca Pellicoro, Bill Manaris
   version 1.0 (February 26, 2007)
   """

   @staticmethod
   def createCSV(fileName, measurements):
      """
      Will take an array of measurements and write the corresponding headers to a csv file.
      """
      if os.path.exists(fileName):
         raise FileExistsError(f"The specified file: {fileName} already exists")

      try:
         with open(fileName, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            headers_row = []
            for measurement in measurements:
               headers = measurement.keysToArray()
               headers_row.extend(headers)

            headers_row.append("Filename")
            writer.writerow(headers_row)

      except Exception as e:
         print(f"createCSV(): an error with file I/O occured, namely \"{e}\"")

   @staticmethod
   def appendCSV(fileName, MIDIFileName, measurements):
      """
      Adds collection of Measurement resuls to a csv file.
      Should work with an existing csv file.
      """
      if not os.path.exists(fileName):
         # if the file does not exist, create it and write the headers
         CSVWriter.createCSV(fileName, measurements)

      try:
         with open(fileName, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            data_row = []
            for measurement in measurements:
               metricResults = measurement.valuesToArray()
               data_row.extend(metricResults)

            data_row.append(MIDIFileName)
            writer.writerow(data_row)

      except Exception as e:
         print(f"appendCSV(): an error with file I/O occured, namely \"{e}\"")

   @staticmethod
   def appendCSV_withHitCount(fileName, MIDIFileName, measurements, hitCount):
      """
      Adds collection of Measurement resuls to a csv file.
      Also appends an extra integer which is the web log hitcount.
      """
      if not os.path.exists(fileName):
         CSVWriter.createCSV(fileName, measurements)

      try:
         with open(fileName, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            data_row = []
            for measurement in measurements:
               metricResults = measurement.valuesToArray()
               data_row.extend(metricResults)

            # The original Java code writes "Filename; HitCount" (implied by logic)
            # but createsCSV only adds "Filename" header.
            # Java: out.write(MIDIFileName + "; "); out.write(hits);
            # This appends two columns at end.

            data_row.append(MIDIFileName)
            data_row.append(hitCount)
            writer.writerow(data_row)

      except Exception as e:
         print(f"an error with file I/O occured: {e}")

   @staticmethod
   def appendConxFile(fileName, measurements, outputClass):
      """
      Append to a file in the conx format (space separated, normalized).
      """
      try:
         with open(fileName, 'a', newline='') as f:
            # Not using csv writer here to match Java manual writing if needed,
            # but Java used space separation.

            row_str = ""
            for measurement in measurements:
               metricResults = measurement.valuesToArray()
               for val in metricResults:
                  # normalize: abs(val) / 10.0
                  # Handle None/NaN? Java code assumes doubles.
                  if val is None: val = 0.0 # Safety fallback
                  conxFormat = abs(val) / 10.0
                  row_str += f"{conxFormat} "

            row_str += f"{outputClass}\n"
            f.write(row_str)

      except Exception as e:
         print(f"an error with file I/O occured: {e}")

   @staticmethod
   def MeasurementsToArray(measurements):
      """
      Will "unpack" an array of measurements into a list.
      """
      results = []
      for measurement in measurements:
         metricResults = measurement.valuesToArray()
         results.extend(metricResults)
      return results
