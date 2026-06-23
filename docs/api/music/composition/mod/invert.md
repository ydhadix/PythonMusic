# invert()

Flip the pitches of a phrase around a center pitch, in place.

```python
Mod.invert(phrase, pitchAxis)
```

A note that is some distance above the center pitch ends up the same distance below it, and vice versa. The order of the notes does not change.

## Parameters

```python
Mod.invert(phrase, pitchAxis, scale=CHROMATIC_SCALE, key=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `phrase` | `Phrase` | _required_ | The phrase to change. |
| `pitchAxis` | `int` | _required_ | The center pitch to flip around, as a MIDI pitch. |
| `scale` | `list[int]` | `CHROMATIC_SCALE` | The scale to keep the flipped pitches in, a list of pitch classes between 0 and 11. If omitted, every pitch is allowed (the chromatic scale). |
| `key` | `int` | `0` | The scale's root pitch class, from 0 to 11, where 0 means C. |
