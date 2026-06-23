# setTarget()

Aim the ramp at a new value, starting from where it is now.

```python
linearramp.setTarget(targetValue)
```

You can also change how long the ramp takes. If the ramp was not running, this starts it.

## Parameters

```python
linearramp.setTarget(targetValue, delay=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `targetValue` | `int or float` | _required_ | The new value to ramp toward. |
| `delay` | `int or float` | `None` | A new length for the ramp, in milliseconds. If omitted, the current length is kept. |
