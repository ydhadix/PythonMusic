# Line

Lines are drawn between a starting point (x1, y1) and an ending point (x2, y2).

## Creating a Line

You can create a Line using the following functions:

```python
line = Line(x1, y1, x2, y2)
```

```python
Line(x1, y1, x2, y2, color, thickness, rotation, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x1` | `int or float` | _required_ | The horizontal position of one end, in pixels. |
| `y1` | `int or float` | _required_ | The vertical position of one end, in pixels. |
| `x2` | `int or float` | _required_ | The horizontal position of the other end, in pixels. |
| `y2` | `int or float` | _required_ | The vertical position of the other end, in pixels. |
| `color` | `Color` | `Color.BLACK` | The color. |
| `thickness` | `int` | `1` | The line thickness, in pixels. |
| `rotation` | `int or float` | `0` | How far to turn the line, in degrees, counter-clockwise. |
| `visibility` | `int` | `100` | How visible the line is, from 0 (invisible) to 100 (fully visible). |

For example,

```python
line = Line(100, 100, 200, 200)
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Line `line` has been created, the following functions are available:

### Position

| Function | Description |
|---|---|
| [`line.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`line.getX()`](getX.md) | Return the object's horizontal position. |
| [`line.getY()`](getY.md) | Return the object's vertical position. |
| [`line.getCenter()`](getCenter.md) | Return the object's center point. |
| [`line.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`line.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`line.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`line.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`line.setY(y)`](setY.md) | Set the object's vertical position. |
| [`line.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`line.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`line.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`line.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`line.getLength()`](getLength.md) | Return the line's length. |
| [`line.getSize()`](getSize.md) | Return the object's width and height. |
| [`line.getWidth()`](getWidth.md) | Return the object's width. |
| [`line.getHeight()`](getHeight.md) | Return the object's height. |
| [`line.setLength(length)`](setLength.md) | Set the line's length. |
| [`line.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`line.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`line.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`line.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`line.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`line.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`line.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`line.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Color

| Function | Description |
|---|---|
| [`line.getColor()`](getColor.md) | Return the shape's color. |
| [`line.getFill()`](getFill.md) | Report whether the shape is filled in. |
| [`line.getThickness()`](getThickness.md) | Return the shape's outline thickness. |
| [`line.setColor()`](setColor.md) | Set the shape's color. |
| [`line.setFill(fill)`](setFill.md) | Set whether the shape is filled in. |
| [`line.setThickness(thickness)`](setThickness.md) | Set the shape's outline thickness. |

### Information

| Function | Description |
|---|---|
| [`line.getEndpoints()`](getEndpoints.md) | Return the object's endpoints. |
| [`line.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`line.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`line.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`line.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`line.contains(x, y)`](contains.md) | Report whether a point lies on the line. |
| [`line.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`line.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`line.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`line.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`line.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`line.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`line.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`line.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`line.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`line.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`line.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`line.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
