# Microtonality

PythonMusic supports [microtonal material](https://en.wikipedia.org/wiki/Microtonal_music).

Microtonality is possible through creating Notes with float numbers as pitches (e.g., 443.1). If a pitch is float, it is considered to be in Hertz. If a pitch is integer, it is considered to be in MIDI (e.g., A4 or 69). In other words, pitch 440.0 is equivalent to pitch 69 (or A4).

For example:

```python
from music import *
 
note = Note(443.1, HN)     # create a note a bit over A4 (440.0)
Play.midi(note)            # and play it!
```

## Microtonality with Audio Instruments

Microtonality works very well with [Audio Samples](performance/audiosample/index.md). Simply create polyphonic material using float numbers as pitches (e.g., 432.3 – that’s in Hz).

Then, play it using [Play.audio()](play/audio.md).

## Microtonality with MIDI Instruments

Microtonality is possible, but limited for [MIDI instruments](play/midi.md).

The MIDI standard does not support microtonality well.

In PythonMusic, microtonal pitches are implemented via MIDI pitch bend. There is only one pitch bend per channel, so you can only play one microtonal note per channel, at a time. If there are concurrent notes (e.g., chords), you need to spread them across different channels (0-8 and 10-15 – since channel 9 is reserved for percussion).  

One way to use microtones with PythonMusic + MIDI:

> Store each concurrent voice in its own [Phrase](transcription/phrase/index.md), and store each Phrase in its own [Part](transcription/part/index.md), using a unique channel (0-8 and 10-15).

Another way:

> Use [Play.noteOn()](play/noteOn.md) interactively, and manually send concurrent notes to different channels.

In summary, the best way to do microtonality is to use [Audio Samples](performance/audiosample/index.md). Simply create polyphonic material using float numbers as pitches. Then, play it via [Play.audio()](play/audio.md).