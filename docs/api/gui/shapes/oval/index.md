# Oval

Ovals are drawn between a starting point (x1, y1) and an ending point (x2, y2).  The oval fills the box, touching the center of each side.

## Creating an Oval

You can create an Oval using the following functions:

```python
oval = Oval(x1, y1, x2, y2)
```

```python
Oval(x1, y1, x2, y2, color, fill, thickness, rotation, visibility)
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
| `visibility` | `int` | `100` | How visible the oval is, from 0 (invisible) to 100 (fully visible). |

For example,

```python
oval = Oval(50, 30, 100, 150)
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once an Oval `oval` has been created, the following functions are available:

### Position

| Function | Description |
|---|---|
| [`oval.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`oval.getX()`](getX.md) | Return the object's horizontal position. |
| [`oval.getY()`](getY.md) | Return the object's vertical position. |
| [`oval.getCenter()`](getCenter.md) | Return the object's center point. |
| [`oval.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`oval.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`oval.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`oval.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`oval.setY(y)`](setY.md) | Set the object's vertical position. |
| [`oval.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`oval.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`oval.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`oval.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`oval.getSize()`](getSize.md) | Return the object's width and height. |
| [`oval.getWidth()`](getWidth.md) | Return the object's width. |
| [`oval.getHeight()`](getHeight.md) | Return the object's height. |
| [`oval.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`oval.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`oval.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`oval.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`oval.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`oval.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`oval.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`oval.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Color

| Function | Description |
|---|---|
| [`oval.getColor()`](getColor.md) | Return the shape's color. |
| [`oval.getFill()`](getFill.md) | Report whether the shape is filled in. |
| [`oval.getThickness()`](getThickness.md) | Return the shape's outline thickness. |
| [`oval.setColor()`](setColor.md) | Set the shape's color. |
| [`oval.setFill(fill)`](setFill.md) | Set whether the shape is filled in. |
| [`oval.setThickness(thickness)`](setThickness.md) | Set the shape's outline thickness. |

### Information

| Function | Description |
|---|---|
| [`oval.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`oval.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`oval.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`oval.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`oval.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`oval.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`oval.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`oval.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`oval.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`oval.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`oval.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`oval.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`oval.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`oval.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`oval.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`oval.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`oval.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`oval.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
