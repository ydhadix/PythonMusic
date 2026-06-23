# Toggle

Create a toggle button that switches on and off with each click.

Toggles are drawn between a starting point (x1, y1) and an ending point (x2, y2).

## Creating a Toggle

You can create a Toggle using the following functions:

```python
Toggle(x1, y1, x2, y2)
```

```python
Toggle(x1, y1, x2, y2, action, foregroundColor, backgroundColor, outlineColor, thickness, rotation, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x1` | `int or float` | _required_ | The horizontal position of the top-left corner, in pixels. |
| `y1` | `int or float` | _required_ | The vertical position of the top-left corner, in pixels. |
| `x2` | `int or float` | _required_ | The horizontal position of the bottom-right corner, in pixels. |
| `y2` | `int or float` | _required_ | The vertical position of the bottom-right corner, in pixels. |
| `action` | `function` | `None` | The function to call when the toggle changes; it receives the new value. |
| `foregroundColor` | `Color` | `Color.RED` | The color when on. |
| `backgroundColor` | `Color` | `Color.BLACK` | The color behind the toggle. |
| `outlineColor` | `Color` | `Color.CLEAR` | The outline color. |
| `thickness` | `int` | `3` | The outline thickness, in pixels. |
| `rotation` | `int or float` | `0` | How far to turn the toggle, in degrees, counter-clockwise. |
| `visibility` | `int` | `100` | How visible the toggle is, from 0 (invisible) to 100 (fully visible). |

For example,

```python title="simpleToggle.py"
--8<-- "examples/_snippets/simpleToggle.py"
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Toggle `toggle` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`toggle.getValue()`](getValue.md) | Report whether the object is currently held down. |
| [`toggle.setValue(newValue)`](setValue.md) | Set whether the object is pressed. |

### Position

| Function | Description |
|---|---|
| [`toggle.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`toggle.getX()`](getX.md) | Return the object's horizontal position. |
| [`toggle.getY()`](getY.md) | Return the object's vertical position. |
| [`toggle.getCenter()`](getCenter.md) | Return the object's center point. |
| [`toggle.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`toggle.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`toggle.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`toggle.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`toggle.setY(y)`](setY.md) | Set the object's vertical position. |
| [`toggle.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`toggle.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`toggle.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`toggle.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`toggle.getSize()`](getSize.md) | Return the object's width and height. |
| [`toggle.getWidth()`](getWidth.md) | Return the object's width. |
| [`toggle.getHeight()`](getHeight.md) | Return the object's height. |
| [`toggle.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`toggle.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`toggle.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`toggle.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`toggle.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`toggle.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`toggle.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`toggle.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Information

| Function | Description |
|---|---|
| [`toggle.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`toggle.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`toggle.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`toggle.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`toggle.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`toggle.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`toggle.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`toggle.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`toggle.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`toggle.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse toggle is pressed on this object. |
| [`toggle.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse toggle is released over this object. |
| [`toggle.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`toggle.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`toggle.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`toggle.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`toggle.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`toggle.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`toggle.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
