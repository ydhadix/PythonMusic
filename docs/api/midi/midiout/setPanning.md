# setPanning()

Set the main stereo position for a channel.

```python
midiout.setPanning(panning)
```

The default is the middle (64). Note that this does not affect a score played through [play()](play.md).

## Parameters

```python
midiout.setPanning(panning, channel=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `panning` | `int` | _required_ | Stereo position from 0 (left) through 64 (center) to 127 (right). |
| `channel` | `int` | `0` | The channel to set, from 0 to 15. |
