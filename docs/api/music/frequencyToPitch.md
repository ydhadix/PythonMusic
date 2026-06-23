# frequencyToPitch()

Convert a frequency to the nearest MIDI pitch plus a pitch bend.

```python
frequencyToPitch(frequency)
```

The pitch bend captures the leftover distance to the exact frequency, for finer
control. A4 (concert pitch, 440 Hz) is pitch 69.

## Parameters

```python
frequencyToPitch(frequency)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `frequency` | `float` | _required_ | The frequency to convert, in hertz (8.17 to 12600.0). |

## Returns

`return pitch, pitchBend`

| Value | Type | Description |
|---|---|---|
| pitch | `int` | The nearest MIDI pitch, from 0 to 127. |
| pitchBend | `int` | The leftover bend to the exact frequency, in pitch bend units from -8191 to 8192, where 0 means no bend. |
