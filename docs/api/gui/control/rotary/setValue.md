# setValue()

Set the rotary's value.

The value is in the knob's own minValue–maxValue range. The knob turns to match, and the update function is called.

## Parameters

Once an object `rotary` has been created, you can use the following function:

```python
rotary.setValue(newValue)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `newValue` | `int or float` | _required_ | The new value, between the rotary's minValue and maxValue. |
