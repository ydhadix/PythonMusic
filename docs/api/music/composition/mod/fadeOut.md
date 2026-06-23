# fadeOut()

Fade the music down from its normal volume to silence, in place.

```python
Mod.fadeOut(material, fadeLength)
```

## Parameters

```python
Mod.fadeOut(material, fadeLength, _endTime=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `material` | `Phrase, Part, or Score` | _required_ | The music to change. |
| `fadeLength` | `int or float` | _required_ | How long the fade lasts, in beats. |
| `_endTime` | `int or float` | `None` | Internal use; leave unset. |
