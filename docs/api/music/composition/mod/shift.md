# shift()

Move every phrase's start time earlier or later, in place.

```python
Mod.shift(material, time)
```

A positive time moves the music later; a negative time moves it earlier, but not before the start of the piece (0.0).

## Parameters

```python
Mod.shift(material, time)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `material` | `Phrase, Part, or Score` | _required_ | The music to change. |
| `time` | `int or float` | _required_ | How far to move the music, in beats. |
