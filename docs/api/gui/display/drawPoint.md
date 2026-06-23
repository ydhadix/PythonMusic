# drawPoint()

Draw a single point straight onto the display.

```python
display.drawPoint(x, y)
```

This draws to the canvas and returns nothing, which is fast and best for shapes you will not change later. To keep a handle you can move or delete, create a Point and [add()](add.md) it instead. Erase these drawings with [clearDrawing()](clearDrawing.md).

## Parameters

```python
display.drawPoint(x, y, color=Color.BLACK)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x` | `int or float` | _required_ | The horizontal position, in pixels. |
| `y` | `int or float` | _required_ | The vertical position, in pixels. |
| `color` | `Color` | `Color.BLACK` | The color. |
