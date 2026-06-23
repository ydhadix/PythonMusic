# add()

Schedule a function for the metronome to call on a given beat.

```python
metronome.add(action)
```

## Parameters

```python
metronome.add(action, parameters=[], desiredBeat=0, repeatFlag=False)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `action` | `function` | _required_ | The function to call. |
| `parameters` | `list` | `[]` | The parameters to pass to the function. |
| `desiredBeat` | `int` | `0` | Which beat to call it on. 0 means the very next beat, 1 the first beat of the measure, 2 the second, and so on. A beat past the end of the measure carries into later measures. |
| `repeatFlag` | `bool` | `False` | Whether to call it every time that beat comes around (True) or just once (False). |
