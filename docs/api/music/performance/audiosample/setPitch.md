# setPitch()

Set the sample's playback pitch, pitch-shifting it from its base pitch.

```python
audiosample.setPitch(pitch)
```

## Parameters

```python
audiosample.setPitch(pitch, voice=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pitch` | `int or float` | _required_ | The new playback pitch, as a MIDI pitch from 0 to 127. |
| `voice` | `int` | `0` | Which voice to set, from 0 to one less than the number of voices. |
