# pitchToFrequency()

Convert a MIDI pitch to its frequency.

```python
pitchToFrequency(pitch)
```

A4 (pitch 69) is concert pitch, 440 Hz.

## Parameters

```python
pitchToFrequency(pitch)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pitch` | `int or float` | _required_ | The MIDI pitch to convert, from 0 to 127. |

## Returns

`return frequency`

| Value | Type | Description |
|---|---|---|
| frequency | `float` | The matching frequency, in hertz (8.17 to 12600.0). |
