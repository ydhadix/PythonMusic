# Zipf Library

Functions for working with Zipf metrics.

## Functions

| Function | Description |
|---|---|
| [`byRank(counts)`](byRank.md) | Measure the Zipf slope of a set of counts, ranked from largest to smallest. |
| [`bySize(sizes, counts)`](bySize.md) | Measure the Zipf slope of a set of counts plotted against given sizes. |
| [`checkRanksAndCounts(ranks, counts)`](checkRanksAndCounts.md) | Check that ranks and counts are valid for a Zipf measurement. |
| [`getSlopeR2(ranks, counts)`](getSlopeR2.md) | Fit a Zipf trendline to a set of ranks and counts. |
| [`measureScore(scores, metrics)`](measureScore.md) | Measure a list of scores against a list of Zipf metrics. |
| [`measureMidi(files, metrics)`](measureMidi.md) | Measure a list of MIDI files against a list of Zipf metrics. |
| [`measureDataByRank(datasets)`](measureDataByRank.md) | Measure a list of count datasets by rank. |
| [`measureDataBySize(datasets)`](measureDataBySize.md) | Measure a list of size-and-count datasets. |
| [`writeCSV(measurements, filename)`](writeCSV.md) | Write measurements to a CSV file. |
