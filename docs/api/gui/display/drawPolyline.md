# drawPolyline()

Draw a connected series of line segments straight onto the display.

```python
display.drawPolyline(xPoints, yPoints)
```

The xPoints and yPoints lists are parallel: the first corner is (xPoints[0], yPoints[0]), the next is (xPoints[1], yPoints[1]), and so on. This draws to the canvas and returns nothing, which is fast and best for shapes you will not change later. To keep a handle you can move or delete, create a Polyline and [add()](add.md) it instead. Erase these drawings with [clearDrawing()](clearDrawing.md).

## Parameters

```python
display.drawPolyline(xPoints, yPoints, color=Color.BLACK, thickness=1, rotation=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `xPoints` | `list[int or float]` | _required_ | The horizontal positions of the corners, in pixels. |
| `yPoints` | `list[int or float]` | _required_ | The vertical positions of the corners, in pixels. |
| `color` | `Color` | `Color.BLACK` | The color. |
| `thickness` | `int` | `1` | The line thickness, in pixels. |
| `rotation` | `int or float` | `0` | How far to turn the shape, in degrees, counter-clockwise. |
