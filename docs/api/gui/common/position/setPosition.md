# setPosition()

Move the object so the top-left corner of its bounding box sits at the given point.

If the object is a [Display](../../display/index.md), this sets the display's position on the screen.

## Parameters

Once an object `item` has been created, you can use the following functions:

```python
item.setPosition(x, y)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x` | `int or float` | _required_ | The new horizontal position, in pixels. |
| `y` | `int or float` | _required_ | The new vertical position, in pixels. |
