# noteOn()

Start a pitch sounding on the device, and leave it sounding.

```python
midiout.noteOn(pitch)
```

The note keeps playing until you stop it with [noteOff()](noteOff.md).

## Parameters

```python
midiout.noteOn(pitch, dynamic=100, channel=0, panning=-1)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pitch` | `int or float` | _required_ | A MIDI pitch from 0 to 127, or a frequency in hertz (8.17 to 12600.0) to reach pitches between the standard notes. |
| `dynamic` | `int` | `100` | How loud the note is, from 0 to 127. |
| `channel` | `int` | `0` | The channel to play on, from 0 to 15. |
| `panning` | `int` | `-1` | Stereo position from 0 (left) to 127 (right); -1 uses the global panning. |
