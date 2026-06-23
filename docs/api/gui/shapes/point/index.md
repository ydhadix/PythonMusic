# Point

Points are drawn at their center point (x, y).  Points behave like [Circles](../circle/index.md) that start with a 0 radius.  Unlike circles, a Point's [getEndpoints()](getEndpoints.md) always returns their center point, even if resized.

## Creating a Point

You can create a Point using the following functions:

```python
point = Point(x, y)
```

```python
Point(x, y, color, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x` | `int or float` | _required_ | The horizontal position, in pixels. |
| `y` | `int or float` | _required_ | The vertical position, in pixels. |
| `color` | `Color` | `Color.BLACK` | The color. |
| `visibility` | `int` | `100` | How visible the point is, from 0 (invisible) to 100 (fully visible). |

For example,

```python
point = Point(50, 50)
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Point `point` has been created, the following functions are available:

### Position

| Function | Description |
|---|---|
| [`point.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`point.getX()`](getX.md) | Return the object's horizontal position. |
| [`point.getY()`](getY.md) | Return the object's vertical position. |
| [`point.getCenter()`](getCenter.md) | Return the object's center point. |
| [`point.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`point.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`point.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`point.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`point.setY(y)`](setY.md) | Set the object's vertical position. |
| [`point.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`point.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`point.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`point.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`point.getSize()`](getSize.md) | Return the object's width and height. |
| [`point.getWidth()`](getWidth.md) | Return the object's width. |
| [`point.getHeight()`](getHeight.md) | Return the object's height. |
| [`point.getRadius()`](getRadius.md) | Return the object's radius. |
| [`point.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`point.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`point.setHeight(height)`](setHeight.md) | Set the object's height. |
| [`point.setRadius(radius)`](setRadius.md) | Set the object's radius. |

### Rotation

| Function | Description |
|---|---|
| [`point.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`point.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`point.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`point.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`point.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Color

| Function | Description |
|---|---|
| [`point.getColor()`](getColor.md) | Return the shape's color. |
| [`point.getFill()`](getFill.md) | Report whether the shape is filled in. |
| [`point.getThickness()`](getThickness.md) | Return the shape's outline thickness. |
| [`point.setColor()`](setColor.md) | Set the shape's color. |
| [`point.setFill(fill)`](setFill.md) | Set whether the shape is filled in. |
| [`point.setThickness(thickness)`](setThickness.md) | Set the shape's outline thickness. |

### Information

| Function | Description |
|---|---|
| [`point.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`point.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`point.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`point.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`point.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`point.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`point.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`point.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`point.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`point.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`point.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`point.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`point.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`point.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`point.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`point.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`point.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`point.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
