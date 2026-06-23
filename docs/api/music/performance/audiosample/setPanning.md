# setPanning()

Set the sample's stereo position.

```python
audiosample.setPanning(panning)
```

## Parameters

```python
audiosample.setPanning(panning, voice=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `panning` | `int` | _required_ | Stereo position from 0 (left) to 127 (right). |
| `voice` | `int` | `0` | Which voice to set, from 0 to one less than the number of voices. |
