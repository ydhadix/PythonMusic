# getEndpoints()

Return the object's current endpoints.

For [Point](../../shapes/point/index.md), [Line](../../shapes/line/index.md), [Polyline](../../shapes/polyline/index.md), and [Polygon](../../shapes/polygon/index.md) objects, the endpoints are the original x and y coordinates used to create the object, accounting for the object moving, resizing, or rotating.

For all other objects, the endpoints are the four corners enclosing the object.  The corners turn with the object, so a rotated object's endpoints are its actual tilted corners.  For the upright box around the object instead, use [getBoundingBox()](getBoundingBox.md).

**NOTE:** This function isn't available to [Displays](../../display/index.md).

## Parameters

Once an object `item` has been created, you can use the following function:

```python
item.getEndpoints()
```

## Returns

`return xPoints, yPoints`

| Value | Type | Description |
|---|---|---|
| xPoints | `list[int or float]` | The horizontal positions of the endpoints, in pixels. |
| yPoints | `list[int or float]` | The vertical positions of the endpoints, in pixels. |
