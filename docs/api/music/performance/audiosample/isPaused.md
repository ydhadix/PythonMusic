# isPaused()

Report whether the sample is currently paused.

```python
audiosample.isPaused()
```

## Parameters

```python
audiosample.isPaused(voice=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `voice` | `int` | `0` | Which voice to check, from 0 to one less than the number of voices. |

## Returns

`return paused`

| Value | Type | Description |
|---|---|---|
| paused | `bool` | True if the sample is paused, False otherwise; None if an error occurs. |
