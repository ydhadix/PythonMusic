# setVolume()

Set the main volume for a channel.

```python
midiout.setVolume(volume)
```

This is the channel's overall volume, separate from how loud each note is played (see [noteOn()](noteOn.md)).

## Parameters

```python
midiout.setVolume(volume, channel=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `volume` | `int` | _required_ | The main volume, from 0 to 127. |
| `channel` | `int` | `0` | The channel to set, from 0 to 15. |
