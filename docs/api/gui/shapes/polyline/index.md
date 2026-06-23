# Polyline

Polylines are a series of connected lines, drawn using two parallel lists of x and y coordinates.  Unlike a [Polygon](../polygon/index.md), the path is open (the last corner is not joined back to the first).

## Creating a Polyline

You can create a Polyline using the following functions:

```python
Polyline(xPoints, yPoints)
```

```python
Polyline(xPoints, yPoints, color, thickness, rotation, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `xPoints` | `list[int or float]` | _required_ | The horizontal positions of the corners, in pixels. |
| `yPoints` | `list[int or float]` | _required_ | The vertical positions of the corners, in pixels. |
| `color` | `Color` | `Color.BLACK` | The color. |
| `thickness` | `int` | `1` | The line thickness, in pixels. |
| `rotation` | `int or float` | `0` | How far to turn the shape, in degrees, counter-clockwise. |
| `visibility` | `int` | `100` | How visible the shape is, from 0 (invisible) to 100 (fully visible). |

For example,

```python
polyline = Polyline([312, 366, 510, 443], [244, 210, 312, 346])
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Polyline `polyline` has been created, the following functions are available:

### Position

| Function | Description |
|---|---|
| [`polyline.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`polyline.getX()`](getX.md) | Return the object's horizontal position. |
| [`polyline.getY()`](getY.md) | Return the object's vertical position. |
| [`polyline.getCenter()`](getCenter.md) | Return the object's center point. |
| [`polyline.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`polyline.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`polyline.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`polyline.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`polyline.setY(y)`](setY.md) | Set the object's vertical position. |
| [`polyline.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`polyline.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`polyline.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`polyline.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`polyline.getSize()`](getSize.md) | Return the object's width and height. |
| [`polyline.getWidth()`](getWidth.md) | Return the object's width. |
| [`polyline.getHeight()`](getHeight.md) | Return the object's height. |
| [`polyline.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`polyline.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`polyline.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`polyline.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`polyline.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`polyline.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`polyline.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`polyline.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Color

| Function | Description |
|---|---|
| [`polyline.getColor()`](getColor.md) | Return the shape's color. |
| [`polyline.getFill()`](getFill.md) | Report whether the shape is filled in. |
| [`polyline.getThickness()`](getThickness.md) | Return the shape's outline thickness. |
| [`polyline.setColor()`](setColor.md) | Set the shape's color. |
| [`polyline.setFill(fill)`](setFill.md) | Set whether the shape is filled in. |
| [`polyline.setThickness(thickness)`](setThickness.md) | Set the shape's outline thickness. |

### Information

| Function | Description |
|---|---|
| [`polyline.getEndpoints()`](getEndpoints.md) | Return the objects's corners. |
| [`polyline.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`polyline.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`polyline.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`polyline.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`polyline.contains(x, y)`](contains.md) | Report whether a point lies inside the polyline. |
| [`polyline.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`polyline.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`polyline.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`polyline.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`polyline.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`polyline.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`polyline.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`polyline.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`polyline.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`polyline.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`polyline.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`polyline.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |