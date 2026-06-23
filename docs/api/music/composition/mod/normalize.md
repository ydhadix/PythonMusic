# normalize()

Scale every note's volume up so the loudest note reaches the maximum, in place.

```python
Mod.normalize(material)
```

The notes keep their relative loudness.

## Parameters

```python
Mod.normalize(material)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `material` | `Phrase, Part, or Score` | _required_ | The music to change. |
