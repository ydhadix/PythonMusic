# setValue()

Set the knob's value.

```python
rotary.setValue(newValue)
```

The value is in the knob's own minValue–maxValue range. The knob turns to match, and the update function is called.

## Parameters

```python
rotary.setValue(newValue)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `newValue` | `int or float` | _required_ | The new value, between minValue and maxValue. |
