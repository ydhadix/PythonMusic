# setValue()

Set the fader's value.

```python
vfader.setValue(newValue)
```

The value is in the fader's own minValue–maxValue range. The fill moves to match, and the update function is called.

## Parameters

```python
vfader.setValue(newValue)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `newValue` | `int or float` | _required_ | The new value, between minValue and maxValue. |
