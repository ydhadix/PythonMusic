# setFunction()

Set the function the timer calls.

```python
timer.setFunction(action)
```

## Parameters

```python
timer.setFunction(action, parameters=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `action` | `function` | _required_ | The function to call; it should accept as many parameters as the parameters list holds. |
| `parameters` | `list` | `None` | The parameters to pass to the function each time it is called. Defaults to none. |
