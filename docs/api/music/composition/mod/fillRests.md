# fillRests()

Replace each note-then-rest with one longer note, in place.

```python
Mod.fillRests(material)
```

Lengthens a note to absorb the rest that follows it and removes the rest, lowering the note count.

## Parameters

```python
Mod.fillRests(material)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `material` | `Phrase, Part, or Score` | _required_ | The music to change. |
