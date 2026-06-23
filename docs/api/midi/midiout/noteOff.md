# noteOff()

Stop a pitch from sounding on the device.

```python
midiout.noteOff(pitch)
```

If the pitch is not sounding on this channel, nothing happens.

## Parameters

```python
midiout.noteOff(pitch, channel=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pitch` | `int or float` | _required_ | A MIDI pitch from 0 to 127, or a frequency in hertz (8.17 to 12600.0). |
| `channel` | `int` | `0` | The channel it is playing on, from 0 to 15. |
