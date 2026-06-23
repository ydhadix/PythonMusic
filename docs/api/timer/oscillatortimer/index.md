# OscillatorTimer

Call a function over and over with a value that oscillates between two bounds.

```python
oscillatorTimer = OscillatorTimer(delay, minValue, maxValue, step, action)
```

An OscillatorTimer moves a value smoothly up and down between a minimum and a maximum,
following a cosine wave, and calls your function with that value every delay
milliseconds. It is handy for fluctuating a sound's volume, panning, or frequency,
among other things. Start it with [start()](start.md), and stop it with [stop()](stop.md).

## Creating an OscillatorTimer

```python
OscillatorTimer(delay, minValue, maxValue, step, action)
```

You can create an OscillatorTimer with the following parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `delay` | `int or float` | _required_ | How long to wait between updates, in milliseconds. |
| `minValue` | `int or float` | _required_ | The lowest value to oscillate down to. |
| `maxValue` | `int or float` | _required_ | The highest value to oscillate up to. |
| `step` | `int or float` | _required_ | How far the value moves each update, from 0 to (maxValue - minValue). |
| `action` | `function` | _required_ | The function to call each update; it receives one parameter, the current value. |

## Functions

Once an OscillatorTimer `oscillatortimer` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`oscillatortimer.start()`](start.md) | Start the oscillator and begin calling your function. |
| [`oscillatortimer.stop()`](stop.md) | Stop the oscillator. |
| [`oscillatortimer.setDelay(delay)`](setDelay.md) | Set how long the oscillator waits between updates. |
| [`oscillatortimer.getDelay()`](getDelay.md) | Return how long the oscillator waits between updates. |
