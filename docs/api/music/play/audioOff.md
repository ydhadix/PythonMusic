# audioOff()

Stop a pitch from sounding on an audio sample.

```python
Play.audioOff(pitch, audioSample)
```

If the pitch is not sounding on this sample, nothing happens.

## Parameters

```python
Play.audioOff(pitch, audioSample, envelope=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pitch` | `int or float` | _required_ | A MIDI pitch from 0 to 127, or a frequency in hertz (8.17 to 12600.0). |
| `audioSample` | `AudioSample` | _required_ | The audio sample the pitch is playing on. |
| `envelope` | `Envelope` | `None` | The same envelope passed to the matching [Play.audioOn()](audioOn.md), so its release can be applied. |
