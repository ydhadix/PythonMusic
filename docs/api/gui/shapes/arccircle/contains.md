# contains()

Report whether a point lies on (or inside) the arc.

```python
arccircle.contains(x, y)
```

For an OPEN arc this tests whether the point is on the arc line; for a CHORD or PIE arc it tests whether the point is inside the closed shape.

## Parameters

```python
arccircle.contains(x, y)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x` | `int or float` | _required_ | The horizontal position to test, in pixels. |
| `y` | `int or float` | _required_ | The vertical position to test, in pixels. |

## Returns

`return contains`

| Value | Type | Description |
|---|---|---|
| contains | `bool` | True if the point is on or inside the arc, False otherwise. |
