# getInstrument()

Return the instrument set for a channel.

```python
Play.getInstrument()
```

## Parameters

```python
Play.getInstrument(channel=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `channel` | `int` | `0` | The channel to read, from 0 to 15. |

## Returns

`return instrument`

| Value | Type | Description |
|---|---|---|
| instrument | `int` | The instrument (timbre), as a MIDI instrument number from 0 to 127. |
