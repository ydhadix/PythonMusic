# drawOval()

Draw an oval straight onto the display.

```python
display.drawOval(x1, y1, x2, y2)
```

The oval fills the box with corners (x1, y1) and (x2, y2). This draws to the canvas and returns nothing, which is fast and best for shapes you will not change later. To keep a handle you can move or delete, create an Oval and [add()](add.md) it instead. Erase these drawings with [clearDrawing()](clearDrawing.md).

## Parameters

```python
display.drawOval(x1, y1, x2, y2, color=Color.BLACK, fill=False, thickness=1, rotation=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x1` | `int or float` | _required_ | The horizontal position of the box's top-left corner, in pixels. |
| `y1` | `int or float` | _required_ | The vertical position of the box's top-left corner, in pixels. |
| `x2` | `int or float` | _required_ | The horizontal position of the box's bottom-right corner, in pixels. |
| `y2` | `int or float` | _required_ | The vertical position of the box's bottom-right corner, in pixels. |
| `color` | `Color` | `Color.BLACK` | The color. |
| `fill` | `bool` | `False` | Whether the oval is filled in (True) or just an outline (False). |
| `thickness` | `int` | `1` | The outline thickness, in pixels. |
| `rotation` | `int or float` | `0` | How far to turn the oval, in degrees, counter-clockwise. |
