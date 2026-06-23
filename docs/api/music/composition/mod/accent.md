# accent()

Make certain beats of each measure louder, in place.

```python
Mod.accent(material, meter)
```

## Parameters

```python
Mod.accent(material, meter, accentedBeats=[0.0], accentAmount=20)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `material` | `Phrase, Part, or Score` | _required_ | The music to change. |
| `meter` | `int or float` | _required_ | The number of beats per measure, for example 4.0. |
| `accentedBeats` | `list[int or float]` | `[0.0]` | Which beats to accent, in beats from the start of the measure. |
| `accentAmount` | `int` | `20` | How much louder to make the accented beats, from 0 to 127. |
