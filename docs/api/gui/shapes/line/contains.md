# contains()

Report whether a point lies on the polyline.

```python
line.contains(x, y)
```

Tests whether the point is on (or very near) the line itself.

## Parameters

```python
line.contains(x, y)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x` | `int or float` | _required_ | The horizontal position to test, in pixels. |
| `y` | `int or float` | _required_ | The vertical position to test, in pixels. |

## Returns

`return contains`

| Value | Type | Description |
|---|---|---|
| contains | `bool` | True if the point is on the polyline, False otherwise. |
