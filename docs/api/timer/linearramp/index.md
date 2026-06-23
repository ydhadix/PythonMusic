# LinearRamp

Slide a value smoothly from one number to another over time, calling a function as it changes.

```python
linearramp = LinearRamp(delay, startValue, endValue, action)
```

A LinearRamp moves a value from a start to an end over a set time, calling your function with the current value at each small step along the way. This is handy for fading volume, moving graphics, and other gradual changes. Start it with [start()](start.md), and aim it somewhere new with [setTarget()](setTarget.md) while it runs.

## Creating a LinearRamp

```python
LinearRamp(delay, startValue, endValue, action, step=10)
```

You can create a LinearRamp with the following parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `delay` | `int or float` | _required_ | How long the whole ramp takes, in milliseconds. |
| `startValue` | `int or float` | _required_ | The value to start from. |
| `endValue` | `int or float` | _required_ | The value to end at. |
| `action` | `function` | _required_ | The function to call as the value changes; it receives one parameter, the current value. |
| `step` | `int` | `10` | How often to update the value and call the function, in milliseconds. |

## Functions

Once a LinearRamp `linearramp` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`linearramp.start()`](start.md) | Start the ramp from its current value toward its target. |
| [`linearramp.stop()`](stop.md) | Stop the ramp where it is. |
| [`linearramp.setTarget(targetValue)`](setTarget.md) | Aim the ramp at a new value, starting from where it is now. |
| [`linearramp.setDuration(delay)`](setDuration.md) | Change how long the ramp takes. |
| [`linearramp.isRunning()`](isRunning.md) | Report whether the ramp is running. |
| [`linearramp.getCurrentValue()`](getCurrentValue.md) | Return the ramp's current value. |
