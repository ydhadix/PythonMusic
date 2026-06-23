# frequency()

Schedule a frequency to play after a delay and last a set time.

```python
Play.frequency(frequency, start, duration)
```

Play only one frequency per channel at a time: since this uses pitch bend, it affects
every other note sounding on the channel.

## Parameters

```python
Play.frequency(frequency, start, duration, velocity=100, channel=0, panning=-1)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `frequency` | `float` | _required_ | The frequency to play, in hertz (8.17 to 12600.0). |
| `start` | `int or float` | _required_ | How long from now the note begins, in milliseconds. |
| `duration` | `int or float` | _required_ | How long the note lasts, in milliseconds. |
| `velocity` | `int` | `100` | How loud the note is, from 0 to 127. |
| `channel` | `int` | `0` | The channel to play on, from 0 to 15. |
| `panning` | `int` | `-1` | Stereo position from 0 (left) to 127 (right); -1 uses the global panning. |
