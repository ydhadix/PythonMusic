# loop()

Play the sample over and over.

```python
audiosample.loop()
```

## Parameters

```python
audiosample.loop(times=-1, start=0, size=-1, voice=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `times` | `int` | `-1` | How many times to repeat; -1 repeats forever. |
| `start` | `int or float` | `0` | Where to start playing, in milliseconds from the beginning of the sample. |
| `size` | `int` | `-1` | How much to play, in milliseconds; -1 plays to the end. |
| `voice` | `int` | `0` | Which voice to play on, from 0 to one less than the number of voices. |
