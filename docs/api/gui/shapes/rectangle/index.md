# Rectangle

Rectangles are drawn between a starting point (x1, y1) and an ending point (x2, y2).

## Creating a Rectangle

You can create a Rectangle using the following functions:

```python
Rectangle(x1, y1, x2, y2)
```

```python
Rectangle(x1, y1, x2, y2, color, fill, thickness, rotation, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x1` | `int or float` | _required_ | The horizontal position of the top-left corner, in pixels. |
| `y1` | `int or float` | _required_ | The vertical position of the top-left corner, in pixels. |
| `x2` | `int or float` | _required_ | The horizontal position of the bottom-right corner, in pixels. |
| `y2` | `int or float` | _required_ | The vertical position of the bottom-right corner, in pixels. |
| `color` | `Color` | `Color.BLACK` | The color. |
| `fill` | `bool` | `False` | Whether the rectangle is filled in (True) or just an outline (False). |
| `thickness` | `int` | `1` | The outline thickness, in pixels. |
| `rotation` | `int or float` | `0` | How far to turn the rectangle, in degrees, counter-clockwise. |
| `visibility` | `int` | `100` | How visible the rectangle is, from 0 (invisible) to 100 (fully visible). |

For example,

```python
rectangle = Rectangle(50, 30, 100, 150)
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Rectangle `rectangle` has been created, the following functions are available:

### Position

| Function | Description |
|---|---|
| [`rectangle.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`rectangle.getX()`](getX.md) | Return the object's horizontal position. |
| [`rectangle.getY()`](getY.md) | Return the object's vertical position. |
| [`rectangle.getCenter()`](getCenter.md) | Return the object's center point. |
| [`rectangle.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`rectangle.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`rectangle.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`rectangle.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`rectangle.setY(y)`](setY.md) | Set the object's vertical position. |
| [`rectangle.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`rectangle.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`rectangle.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`rectangle.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`rectangle.getSize()`](getSize.md) | Return the object's width and height. |
| [`rectangle.getWidth()`](getWidth.md) | Return the object's width. |
| [`rectangle.getHeight()`](getHeight.md) | Return the object's height. |
| [`rectangle.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`rectangle.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`rectangle.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`rectangle.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`rectangle.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`rectangle.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`rectangle.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`rectangle.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Color

| Function | Description |
|---|---|
| [`rectangle.getColor()`](getColor.md) | Return the shape's color. |
| [`rectangle.getFill()`](getFill.md) | Report whether the shape is filled in. |
| [`rectangle.getThickness()`](getThickness.md) | Return the shape's outline thickness. |
| [`rectangle.setColor()`](setColor.md) | Set the shape's color. |
| [`rectangle.setFill(fill)`](setFill.md) | Set whether the shape is filled in. |
| [`rectangle.setThickness(thickness)`](setThickness.md) | Set the shape's outline thickness. |

### Information

| Function | Description |
|---|---|
| [`rectangle.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`rectangle.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`rectangle.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`rectangle.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`rectangle.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`rectangle.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`rectangle.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`rectangle.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`rectangle.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`rectangle.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`rectangle.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`rectangle.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`rectangle.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`rectangle.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`rectangle.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`rectangle.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`rectangle.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`rectangle.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |