# setValue()

Set the tracker's position within the pad.

Positions outside the pad are clamped to its edges. Moves the tracker and calls the update function.

## Parameters

Once an object `xypad` has been created, you can use the following function:

```python
xypad.setValue(x, y)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x` | `int or float` | _required_ | The new horizontal position within the pad, in pixels. |
| `y` | `int or float` | _required_ | The new vertical position within the pad, in pixels. |
