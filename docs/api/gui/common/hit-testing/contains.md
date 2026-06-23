# contains()

Report whether a point lies inside the object.

## Parameters

Once an object `item` has been created, you can use the following function:

```python
item.contains(x, y)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x` | `int or float` | _required_ | The horizontal position to test, in pixels. |
| `y` | `int or float` | _required_ | The vertical position to test, in pixels. |

## Returns

`return contains`

| Value | Type | Description |
|---|---|---|
| contains | `bool` | `True` if the point is inside the object, `False` otherwise. |
