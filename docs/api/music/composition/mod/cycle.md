# cycle()

Repeat a phrase until it holds a set number of notes, in place.

```python
Mod.cycle(phrase, numberOfNotes)
```

Like [Mod.repeat()](repeat.md), but the last repetition may be cut short once the note count is reached.

## Parameters

```python
Mod.cycle(phrase, numberOfNotes)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `phrase` | `Phrase` | _required_ | The phrase to change. |
| `numberOfNotes` | `int` | _required_ | How many notes the phrase should end up with. |
