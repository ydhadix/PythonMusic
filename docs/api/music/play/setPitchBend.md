# setPitchBend()

Set the pitch bend for a channel, used for notes played next.

```python
Play.setPitchBend()
```

## Parameters

```python
Play.setPitchBend(bend=0, channel=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bend` | `int` | `0` | How far to bend the pitch, in pitch bend units from -8191 (full down) to 8192 (full up), where 0 means no bend. |
| `channel` | `int` | `0` | The channel to set, from 0 to 15. |
