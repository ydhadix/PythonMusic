# elongate()

Stretch or squeeze every note's length by a scaling factor, in place.

```python
Mod.elongate(material, scaleFactor)
```

A factor above 1.0 makes the music longer (slower); below 1.0 makes it shorter (faster). For example, 0.5 halves every duration.

## Parameters

```python
Mod.elongate(material, scaleFactor)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `material` | `Note, Phrase, Part, or Score` | _required_ | The music to change. |
| `scaleFactor` | `int or float` | _required_ | The factor to multiply every duration by. |
