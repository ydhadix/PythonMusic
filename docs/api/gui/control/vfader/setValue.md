# setValue()

Set the fader's value.

The value is in the fader's own minValue–maxValue range. The fill moves to match, and the update function is called.

## Parameters

Once an object `fader` has been created, you can use the following function:

```python
fader.setValue(newValue)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `newValue` | `int or float` | _required_ | The new value, between the fader's minValue and maxValue. |
