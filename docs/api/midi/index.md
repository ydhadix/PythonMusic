# MIDI Library

```python
from midi import *
```

The MIDI library supports communication with MIDI controllers and devices.

| Contents | Description |
|---|---|
| [MidiIn](midiin/index.md) | Receive MIDI messages from an input device. |
| [MidiOut](midiout/index.md) | Send MIDI messages to an output device or synthesizer. |
| [MIDI Event Constants](constants.md) | Useful constants for assigning MIDI `eventType` values. |

The MIDI library provides two types of objects:

[MidiIn](midiin/index.md) objects and [MidiOut](midiout/index.md) objects:

- [MidiIn](midiin/index.md) objects may be used in your programs to get input from MIDI devices that generate input events (e.g., a MIDI guitar, keyboard, or control surface).

- [MidiOut](midiout/index.md) objects may be used in your programs to send output to MIDI devices that accept output events (e.g., an external MIDI synthesizer).

MIDI devices need to be connected (via USB cable) to your computer.

**NOTE:** If your MIDI device does not have a USB connection, use a [MIDI-to-USB adaptor](https://www.amazon.com/M-Audio-Midisport-Portable-Interface-connection/dp/B00007JRBM).
