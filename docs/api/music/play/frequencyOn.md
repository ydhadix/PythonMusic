# frequencyOn()

Start a frequency sounding, and leave it sounding.

```python
Play.frequencyOn(frequency)
```

Stop it with [Play.frequencyOff()](frequencyOff.md). Play only one frequency per channel at a time:
since this uses pitch bend, it affects every other note sounding on the channel.

## Parameters

```python
Play.frequencyOn(frequency, velocity=100, channel=0, panning=-1)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `frequency` | `float` | _required_ | The frequency to play, in hertz (8.17 to 12600.0). |
| `velocity` | `int` | `100` | How loud the note is, from 0 to 127. |
| `channel` | `int` | `0` | The channel to play on, from 0 to 15. |
| `panning` | `int` | `-1` | Stereo position from 0 (left) to 127 (right); -1 uses the global panning. |
