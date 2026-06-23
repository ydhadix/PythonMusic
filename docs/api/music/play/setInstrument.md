# setInstrument()

Set the instrument for a channel.

```python
Play.setInstrument(instrument)
```

Notes played on this channel will sound using this instrument.

## Parameters

```python
Play.setInstrument(instrument, channel=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `instrument` | `int` | _required_ | The instrument (timbre), as a MIDI instrument number from 0 to 127. |
| `channel` | `int` | `0` | The channel to set, from 0 to 15. |
