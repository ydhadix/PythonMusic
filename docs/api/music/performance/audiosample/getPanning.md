# getPanning()

Return the sample's stereo position.

```python
audiosample.getPanning()
```

## Parameters

```python
audiosample.getPanning(voice=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `voice` | `int` | `0` | Which voice to read, from 0 to one less than the number of voices. |

## Returns

`return panning`

| Value | Type | Description |
|---|---|---|
| panning | `int` | Stereo position from 0 (left) to 127 (right); None if an error occurs. |
