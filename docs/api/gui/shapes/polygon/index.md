# Polygon

Polygons are closed shapes, drawn using two parallel lists of x and y coordinates.  Unlike a [Polyline](../polyline/index.md), the shape is closed (the last corner joins back to the first).

## Creating a Polygon

You can create a Polygon using the following functions:

```python
Polygon(xPoints, yPoints)
```

```python
Polygon(xPoints, yPoints, color, fill, thickness, rotation, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `xPoints` | `list[int or float]` | _required_ | The horizontal positions of the corners, in pixels. |
| `yPoints` | `list[int or float]` | _required_ | The vertical positions of the corners, in pixels. |
| `color` | `Color` | `Color.BLACK` | The color. |
| `fill` | `bool` | `False` | Whether the polygon is filled in (True) or just an outline (False). |
| `thickness` | `int` | `1` | The outline thickness, in pixels. |
| `rotation` | `int or float` | `0` | How far to turn the polygon, in degrees, counter-clockwise. |
| `visibility` | `int` | `100` | How visible the polygon is, from 0 (invisible) to 100 (fully visible). |

For example,

```python
polygon = Polygon([312, 366, 510, 443], [244, 210, 312, 346])
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Polygon `polygon` has been created, the following functions are available:

### Position

| Function | Description |
|---|---|
| [`polygon.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`polygon.getX()`](getX.md) | Return the object's horizontal position. |
| [`polygon.getY()`](getY.md) | Return the object's vertical position. |
| [`polygon.getCenter()`](getCenter.md) | Return the object's center point. |
| [`polygon.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`polygon.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`polygon.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`polygon.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`polygon.setY(y)`](setY.md) | Set the object's vertical position. |
| [`polygon.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`polygon.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`polygon.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`polygon.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`polygon.getSize()`](getSize.md) | Return the object's width and height. |
| [`polygon.getWidth()`](getWidth.md) | Return the object's width. |
| [`polygon.getHeight()`](getHeight.md) | Return the object's height. |
| [`polygon.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`polygon.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`polygon.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`polygon.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`polygon.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`polygon.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`polygon.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`polygon.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Color

| Function | Description |
|---|---|
| [`polygon.getColor()`](getColor.md) | Return the shape's color. |
| [`polygon.getFill()`](getFill.md) | Report whether the shape is filled in. |
| [`polygon.getThickness()`](getThickness.md) | Return the shape's outline thickness. |
| [`polygon.setColor()`](setColor.md) | Set the shape's color. |
| [`polygon.setFill(fill)`](setFill.md) | Set whether the shape is filled in. |
| [`polygon.setThickness(thickness)`](setThickness.md) | Set the shape's outline thickness. |

### Information

| Function | Description |
|---|---|
| [`polygon.getEndpoints()`](getEndpoints.md) | Return the objects's corners. |
| [`polygon.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`polygon.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`polygon.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`polygon.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`polygon.contains(x, y)`](contains.md) | Report whether a point lies inside the polygon. |
| [`polygon.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`polygon.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`polygon.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`polygon.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`polygon.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`polygon.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`polygon.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`polygon.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`polygon.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`polygon.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`polygon.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`polygon.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
