# Timer

Schedule a function to run after a delay, or to repeat at a fixed interval.

```python
timer = Timer(timeInterval, action)
```

A Timer waits the given interval, then calls your function, and can either stop or repeatedly call it at that interval. Start it with [start()](start.md), and stop it with [stop()](stop.md).

For example:

```python title="simpleTimer1.py"
--8<-- "examples/_snippets/simpleTimer1.py"
```

will print “It’s ticking…” continuously, every half second.

## Creating a Timer

```python
Timer(timeInterval, action, parameters=None, repeat=True)
```

You can create a Timer with the following parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `timeInterval` | `int or float` | _required_ | How long to wait before each call, in milliseconds. |
| `action` | `function` | _required_ | The function to call; it should accept as many parameters as the `parameters` list holds. |
| `parameters` | `list` | `None` | The parameters to pass to the function each time it is called. |
| `repeat` | `bool` | `True` | Whether to keep calling the function at the interval (True) or call it just once (False). |

For example,

```python title="simpleTimer2.py"
--8<-- "examples/_snippets/simpleTimer2.py"
```

This creates a Timer t, which every 500 milliseconds (i.e., half second) calls function Play.noteOn(A4) repeatedly. Notice that the parameters to the function as provided as a separate list (i.e., [A4] above).

Remember that for a timer to begin ticking, it needs to be started:

```python
t.start()
```

Here is one more example, involving graphics animation:

```python title="simpleTimer3.py"
--8<-- "examples/_snippets/simpleTimer3.py"
```

## Functions

Once a Timer `timer` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`timer.start()`](start.md) | Start the timer. |
| [`timer.stop()`](stop.md) | Stop the timer. |
| [`timer.getDelay()`](getDelay.md) | Return the timer's interval. |
| [`timer.setDelay(timeInterval)`](setDelay.md) | Set the timer's interval. |
| [`timer.isRunning()`](isRunning.md) | Report whether the timer is running. |
| [`timer.setFunction(action)`](setFunction.md) | Set the function the timer calls. |
| [`timer.getRepeat()`](getRepeat.md) | Report whether the timer repeats. |
| [`timer.setRepeat(repeat)`](setRepeat.md) | Set whether the timer repeats. |
