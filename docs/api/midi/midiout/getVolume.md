# getVolume()

Return the main volume for a channel.

```python
midiout.getVolume()
```

## Parameters

```python
midiout.getVolume(channel=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `channel` | `int` | `0` | The channel to read, from 0 to 15. |

## Returns

`return volume`

| Value | Type | Description |
|---|---|---|
| volume | `int` | The main volume, from 0 to 127. |
