# transpose()

Shift the pitch of every note, in place.

```python
Mod.transpose(material, steps)
```

With no scale, steps are semitones (for example, 12 raises everything by an octave). With a scale and key, steps are scale degrees instead, keeping the music in that key.

## Parameters

```python
Mod.transpose(material, steps, scale=CHROMATIC_SCALE, key=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `material` | `Note, Phrase, Part, or Score` | _required_ | The music to change. |
| `steps` | `int` | _required_ | How far to shift, in semitones, or in scale degrees when a scale is given. |
| `scale` | `list[int]` | `CHROMATIC_SCALE` | The scale to shift within, a list of pitch classes between 0 and 11. If omitted, the shift is chromatic (by semitones). |
| `key` | `int` | `0` | The scale's root pitch class, from 0 to 11, where 0 means C. |
