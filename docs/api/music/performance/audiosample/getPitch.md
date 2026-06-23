# getPitch()

Return the sample's current playback pitch.

```python
audiosample.getPitch()
```

This may differ from the sample's base pitch if it has been pitch-shifted.

## Parameters

```python
audiosample.getPitch(voice=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `voice` | `int` | `0` | Which voice to read, from 0 to one less than the number of voices. |

## Returns

`return pitch`

| Value | Type | Description |
|---|---|---|
| pitch | `int` | The current playback pitch, as a MIDI pitch from 0 to 127; None if an error occurs. |
