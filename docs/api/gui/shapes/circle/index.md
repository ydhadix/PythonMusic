# Circle

Circles are drawn with a radius around a center point (x, y).

## Creating a Circle

You can create a Circle using the following functions:

```python
Circle(x, y, radius)
```

```python
Circle(x, y, radius, color, fill, thickness, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x` | `int or float` | _required_ | The horizontal position of the center, in pixels. |
| `y` | `int or float` | _required_ | The vertical position of the center, in pixels. |
| `radius` | `int or float` | _required_ | The radius, in pixels. |
| `color` | `Color` | `Color.BLACK` | The color. |
| `fill` | `bool` | `False` | Whether the circle is filled in (True) or just an outline (False). |
| `thickness` | `int` | `1` | The outline thickness, in pixels. |
| `visibility` | `int` | `100` | How visible the circle is, from 0 (invisible) to 100 (fully visible). |

For example,

```python
circle = Circle(50, 50, 5)
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Circle `circle` has been created, the following functions are available:

### Position

| Function | Description |
|---|---|
| [`circle.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`circle.getX()`](getX.md) | Return the object's horizontal position. |
| [`circle.getY()`](getY.md) | Return the object's vertical position. |
| [`circle.getCenter()`](getCenter.md) | Return the object's center point. |
| [`circle.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`circle.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`circle.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`circle.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`circle.setY(y)`](setY.md) | Set the object's vertical position. |
| [`circle.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`circle.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`circle.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`circle.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`circle.getSize()`](getSize.md) | Return the object's width and height. |
| [`circle.getWidth()`](getWidth.md) | Return the object's width. |
| [`circle.getHeight()`](getHeight.md) | Return the object's height. |
| [`circle.getRadius()`](getRadius.md) | Return the object's radius. |
| [`circle.setSize(width, height)`](setSize.md) | Set the object's size. |
| [`circle.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`circle.setHeight(height)`](setHeight.md) | Set the object's height. |
| [`circle.setRadius(radius)`](setRadius.md) | Set the object's radius. |

### Rotation

| Function | Description |
|---|---|
| [`circle.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`circle.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`circle.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`circle.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`circle.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Color

| Function | Description |
|---|---|
| [`circle.getColor()`](getColor.md) | Return the shape's color. |
| [`circle.getFill()`](getFill.md) | Report whether the shape is filled in. |
| [`circle.getThickness()`](getThickness.md) | Return the shape's outline thickness. |
| [`circle.setColor()`](setColor.md) | Set the shape's color. |
| [`circle.setFill(fill)`](setFill.md) | Set whether the shape is filled in. |
| [`circle.setThickness(thickness)`](setThickness.md) | Set the shape's outline thickness. |

### Information

| Function | Description |
|---|---|
| [`circle.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`circle.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`circle.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`circle.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`circle.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`circle.intersects(other)`](intersects.md) | Report whether this circle overlaps another object. |
| [`circle.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`circle.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`circle.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`circle.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`circle.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`circle.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`circle.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`circle.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`circle.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`circle.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`circle.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`circle.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
