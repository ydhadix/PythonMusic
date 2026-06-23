# play()

Play the sample once.

```python
audiosample.play()
```

## Parameters

```python
audiosample.play(start=0, size=-1, voice=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `start` | `int or float` | `0` | Where to start playing, in milliseconds from the beginning of the sample. |
| `size` | `int` | `-1` | How much to play, in milliseconds; -1 plays to the end. |
| `voice` | `int` | `0` | Which voice to play on, from 0 to one less than the number of voices. |
