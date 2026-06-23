# code()

Run your own functions in time with music library material.

```python
Play.code(material, actions)
```

Instead of making sound, each note triggers a function. The note's channel chooses
which function in actions to call, so actions needs one function per channel used.

## Parameters

```python
Play.code(material, actions)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `material` | `Note, Phrase, Part, or Score` | _required_ | The music whose notes drive the timing. |
| `actions` | `list[function]` | _required_ | The functions to call, one per channel. |
