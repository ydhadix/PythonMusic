# getFrameRate()

Return the sample's recording rate.

```python
audiosample.getFrameRate()
```

The rate is fixed by the audio file and is the same for every voice. To change how the sample sounds, use [setFrequency()](setFrequency.md) or [setPitch()](setPitch.md) instead.

## Returns

`return frameRate`

| Value | Type | Description |
|---|---|---|
| frameRate | `float` | The recording rate, in hertz, for example 44100.0; None if an error occurs. |
