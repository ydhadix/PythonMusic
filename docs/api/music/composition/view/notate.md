# notate()

Show the music as staff notation.

```python
View.notate(material)
```

Notation handles only a single phrase at a time (use [Mod.consolidate()](../mod/consolidate.md) to combine a part's phrases first). It also lets you enter music as notation and save it.

## Parameters

```python
View.notate(material, writeToFile=False)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `material` | `Note, Phrase, Part, or Score` | _required_ | The music to show. |
| `writeToFile` | `bool` | `False` | Whether to also save the notation to a file. |
