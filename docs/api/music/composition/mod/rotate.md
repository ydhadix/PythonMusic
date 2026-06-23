# rotate()

Shift the notes around the phrase, in place.

```python
Mod.rotate(phrase)
```

Each shift moves the last note to the front, so the first note becomes the second, and so on.

## Parameters

```python
Mod.rotate(phrase, times=1)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `phrase` | `Phrase` | _required_ | The phrase to change. |
| `times` | `int` | `1` | How many notes to shift by. |
