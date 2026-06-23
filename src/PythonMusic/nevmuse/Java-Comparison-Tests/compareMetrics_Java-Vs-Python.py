"""
Compare two metrics CSV files cell by cell and compute statistics.
Tracks average difference, standard deviation, and maximum difference.
"""

import csv
import numpy as np
from pathlib import Path
from datetime import datetime
import sys
import re


def compareMetricsCsv(file1Path, file2Path, outputFile=None):
   """
   Compare two CSV files cell by cell and compute statistics.

   Args:
      file1Path: Path to first CSV file (new/comparison version)
      file2Path: Path to second CSV file (original version)
      outputFile: Optional file object to write output to

   Returns:
      Dictionary with statistics about the differences
   """

   def printAndLog(message=""):
      """Print to console and optionally to file"""
      print(message)
      if outputFile:
         outputFile.write(message + "\n")

   # read both CSV files
   with open(file1Path, 'r', encoding='utf-8') as f1:
      reader1 = csv.reader(f1)
      headers1 = next(reader1)
      rows1 = list(reader1)

   with open(file2Path, 'r', encoding='utf-8') as f2:
      reader2 = csv.reader(f2)
      headers2 = next(reader2)
      rows2 = list(reader2)

   # verify headers match
   if headers1 != headers2:
      printAndLog("WARNING: Headers do not match!")
      printAndLog(f"File 1 has {len(headers1)} columns")
      printAndLog(f"File 2 has {len(headers2)} columns")
      return None

   printAndLog(f"Headers match: {len(headers1)} columns")
   printAndLog(f"File 1 rows: {len(rows1)}")
   printAndLog(f"File 2 rows: {len(rows2)}")

   # verify same number of rows
   if len(rows1) != len(rows2):
      printAndLog("WARNING: Different number of rows!")
      return None

   # collect all numeric differences
   allDifferences = []
   maxDifference = 0.0
   maxDifferenceLocation = None

   # statistics by column
   columnStats = {}
   for colIdx, colName in enumerate(headers1):
      columnStats[colName] = []

   # statistics by metric type
   metricTypeStats = {}

   # compare each cell
   totalCells = 0
   numericCells = 0
   identicalCells = 0

   for rowIdx, (row1, row2) in enumerate(zip(rows1, rows2)):
      if len(row1) != len(row2):
         printAndLog(f"WARNING: Row {rowIdx} has different number of columns!")
         continue

      for colIdx, (val1, val2) in enumerate(zip(row1, row2)):
         totalCells += 1
         colName = headers1[colIdx]

         # try to compare as numbers
         try:
            num1 = float(val1)
            num2 = float(val2)
            numericCells += 1

            # compute absolute difference
            diff = abs(num1 - num2)
            allDifferences.append(diff)
            columnStats[colName].append(diff)

            # extract metric type from column name (e.g., "PitchDuration_0_Slope" -> "PitchDuration")
            metricType = colName.split('_')[0]
            if metricType not in metricTypeStats:
               metricTypeStats[metricType] = []
            metricTypeStats[metricType].append(diff)

            # track maximum difference
            if diff > maxDifference:
               maxDifference = diff
               maxDifferenceLocation = (rowIdx, colIdx, colName, num1, num2)

            # track identical cells
            if diff < 1e-10:   # essentially zero
               identicalCells += 1

         except ValueError:
            # non-numeric cell (like filename), check if identical
            if val1 == val2:
               identicalCells += 1

   # compute statistics
   if len(allDifferences) == 0:
      printAndLog("No numeric differences found!")
      return None

   avgDifference = np.mean(allDifferences)
   stdDeviation = np.std(allDifferences)
   medianDifference = np.median(allDifferences)

   # print results
   printAndLog()
   printAndLog("=" * 80)
   printAndLog("OVERALL STATISTICS")
   printAndLog("=" * 80)
   printAndLog()
   printAndLog(f"  Total cells compared:     {totalCells:>8,}")
   printAndLog(f"  Numeric cells:            {numericCells:>8,}")
   printAndLog(f"  Identical cells:          {identicalCells:>8,}  ({100*identicalCells/totalCells:>5.2f}%)")
   printAndLog(f"  Different cells:          {totalCells-identicalCells:>8,}  ({100*(totalCells-identicalCells)/totalCells:>5.2f}%)")
   printAndLog()
   printAndLog("  Difference Metrics:")
   printAndLog(f"    Average difference:     {avgDifference:>12.6f}")
   printAndLog(f"    Median difference:      {medianDifference:>12.6f}")
   printAndLog(f"    Std deviation:          {stdDeviation:>12.6f}")
   printAndLog(f"    Maximum difference:     {maxDifference:>12.6f}")

   if maxDifferenceLocation:
      rowIdx, colIdx, colName, val1, val2 = maxDifferenceLocation
      printAndLog()
      printAndLog("  Maximum Difference Details:")
      printAndLog(f"    Row:                    {rowIdx + 2} (CSV line {rowIdx + 2})")
      printAndLog(f"    Column:                 {colIdx}")
      printAndLog(f"    Column name:            {colName}")
      printAndLog(f"    Python value:           {val1}")
      printAndLog(f"    Java value:             {val2}")
      printAndLog(f"    Absolute difference:    {abs(val1 - val2):.10f}")

   # find columns with largest average differences
   printAndLog()
   printAndLog("=" * 80)
   printAndLog("TOP 10 COLUMNS WITH LARGEST AVERAGE DIFFERENCES")
   printAndLog("=" * 80)
   printAndLog()

   columnAvgDiffs = {}
   for colName, diffs in columnStats.items():
      if len(diffs) > 0:
         columnAvgDiffs[colName] = np.mean(diffs)

   sortedColumns = sorted(columnAvgDiffs.items(), key=lambda x: x[1], reverse=True)
   for rank, (colName, avgDiff) in enumerate(sortedColumns[:10], 1):
      printAndLog(f"  {rank:2d}. {colName:55s}  {avgDiff:.8f}")

   # find columns with smallest average differences (most accurate)
   printAndLog()
   printAndLog("=" * 80)
   printAndLog("TOP 10 COLUMNS WITH SMALLEST AVERAGE DIFFERENCES (Most Accurate)")
   printAndLog("=" * 80)
   printAndLog()

   for rank, (colName, avgDiff) in enumerate(reversed(sortedColumns[-10:]), 1):
      printAndLog(f"  {rank:2d}. {colName:55s}  {avgDiff:.8f}")

   # analyze by metric type
   printAndLog()
   printAndLog("=" * 80)
   printAndLog("DIFFERENCES BY METRIC TYPE")
   printAndLog("=" * 80)
   printAndLog()

   metricTypeAvgs = {}
   for metricType, diffs in metricTypeStats.items():
      if len(diffs) > 0:
         metricTypeAvgs[metricType] = {
            'avg': np.mean(diffs),
            'max': np.max(diffs),
            'median': np.median(diffs),
            'std': np.std(diffs),
            'count': len(diffs)
         }

   sortedMetricTypes = sorted(metricTypeAvgs.items(), key=lambda x: x[1]['max'], reverse=True)

   printAndLog(f"{'Metric Type':<30} {'Max Diff':>12} {'Avg Diff':>12} {'Median':>12} {'Std Dev':>12} {'Count':>8}")
   printAndLog("-" * 80)
   for metricType, stats in sortedMetricTypes:
      printAndLog(f"{metricType:<30} {stats['max']:>12.6f} {stats['avg']:>12.6f} {stats['median']:>12.6f} {stats['std']:>12.6f} {stats['count']:>8,}")

   return {
      'avgDifference': avgDifference,
      'stdDeviation': stdDeviation,
      'maxDifference': maxDifference,
      'medianDifference': medianDifference,
      'totalCells': totalCells,
      'numericCells': numericCells,
      'identicalCells': identicalCells,
      'columnStats': columnStats,
      'metricTypeStats': metricTypeStats
   }


if __name__ == "__main__":
   # get script directory to make paths relative to script location
   scriptDir = Path(__file__).parent

   # define file paths relative to script location
   newFile = scriptDir / "Bach AoF Fugues_metrics.csv"
   originalFile = scriptDir / "ORIGINAL-JAVA_Bach AoF Fugues_metrics.csv"

   # create results directory if it doesn't exist
   resultsDir = scriptDir / "results"
   resultsDir.mkdir(exist_ok=True)

   # create timestamped output filename
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   outputFilename = resultsDir / f"comparison_{timestamp}.txt"

   print("=" * 80)
   print("METRICS COMPARISON: Python Implementation vs Java Implementation")
   print("=" * 80)
   print()
   print(f"Python results file:  {newFile.name}")
   print(f"Java results file:    {originalFile.name}")
   print(f"Output file:          {outputFilename.relative_to(scriptDir)}")
   print()

   # verify files exist
   if not newFile.exists():
      print(f"ERROR: File not found: {newFile}")
      sys.exit(1)
   if not originalFile.exists():
      print(f"ERROR: File not found: {originalFile}")
      sys.exit(1)

   # run comparison and save to file
   with open(outputFilename, 'w', encoding='utf-8') as outFile:
      # write header to file
      outFile.write("=" * 80 + "\n")
      outFile.write("METRICS COMPARISON: Python Implementation vs Java Implementation\n")
      outFile.write("=" * 80 + "\n")
      outFile.write(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
      outFile.write(f"Python results file:  {newFile.name}\n")
      outFile.write(f"Java results file:    {originalFile.name}\n")
      outFile.write("\n")

      # run comparison
      results = compareMetricsCsv(newFile, originalFile, outFile)

   if results:
      print()
      print("=" * 80)
      print("COMPARISON COMPLETE!")
      print("=" * 80)
      print(f"\nResults saved to: {outputFilename}")
   else:
      print("\nComparison failed!")
      sys.exit(1)
