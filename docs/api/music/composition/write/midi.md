# midi()

Write music library material to a MIDI file.

```python
Write.midi(material, filename)
```

If the file already exists, it is overwritten.

## Parameters

```python
Write.midi(material, filename)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `material` | `Note, Phrase, Part, or Score` | _required_ | The music to write. |
| `filename` | `str` | _required_ | The MIDI file to write (a .mid file). |
