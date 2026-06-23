# Pitch and Frequency

Pitch and frequency are two ways to communicate how high or low a note sounds. [Pitch](https://en.wikipedia.org/wiki/Pitch_(music)) is how humans perceive change in how high or low a sound is (e.g., MIDI pitch 0 to 127, with A4 = 69). [Frequency](https://en.wikipedia.org/wiki/Frequency) is a physical measurement of how fast a sound wave vibrates.

**NOTE:** MIDI pitch A4 (69) corresponds to 440 Hertz in frequency.

The relationship between pitch and frequency is logarithmic / exponential.

**NOTE:** One octave change in pitch (e.g., A4 to A5), corresponds to a doubling (or halving) of frequency. For example:

- A4 is 69 in pitch, and 440.0 Hz in frequency
- A5 is 81 (69 + 12) in pitch, and 880.0 Hz (440.0 * 2) in frequency
- A3 is 57 (69 – 12) in pitch, and 220.0 Hz (440.0 / 2) in frequency

## Conversion between Pitch and Frequency

The music library provides two functions to convert between pitch (0-127) and frequency (in Hertz):

| Function | Description |
|---|---|
| [pitchToFrequency(pitch)](pitchToFrequency.md) | Converts MIDI pitch (0-127) to frequency (in Hertz). |
| [frequencyToPitch(frequency)](frequencyToPitch.md) | Converts frequency (in Hertz) to MIDI pitch (0-127) |

```python
# convert MIDI pitches to frequencies
>>> pitchToFrequency(A4)
440.0
>>> pitchToFrequency(C4)
261.6255653005986
>>> pitchToFrequency(E4)
329.6275569128699

# convert frequencies to MIDI pitches
>>> frequencyToPitch(440.0)
(69, 0)
>>> frequencyToPitch(443.5)
(69, 562)
>>> frequencyToPitch(438.5)
(69, -242)
 
# capture values in variables
>>> pitch, pitchBend = frequencyToPitch(438.5)   
>>> pitch
69
>>> pitchBend
-242
```

This returns the closest MIDI pitch (0-127), and the remaining pitch bend for finer (microtonal) control. Pitch bend corresponds to +/- 2 half tones, and ranges from -8191 to +8192 (0 means no pitch bend).

**NOTE:** [Note](transcription/note/index.md) objects may be generated with either pitch or frequency values.