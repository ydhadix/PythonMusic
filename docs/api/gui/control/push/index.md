# Push

Create a push-and-hold button.

Push buttons are drawn between a starting point (x1, y1) and an ending point (x2, y2).  The button is on (True) only while it is held down.

## Creating a Push

You can create a Push using the following functions:

```python
Push(x1, y1, x2, y2)
```

```python
Push(x1, y1, x2, y2, action, foregroundColor, backgroundColor, outlineColor, thickness, rotation, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x1` | `int or float` | _required_ | The horizontal position of the top-left corner, in pixels. |
| `y1` | `int or float` | _required_ | The vertical position of the top-left corner, in pixels. |
| `x2` | `int or float` | _required_ | The horizontal position of the bottom-right corner, in pixels. |
| `y2` | `int or float` | _required_ | The vertical position of the bottom-right corner, in pixels. |
| `action` | `function` | `None` | The function to call when the button is pressed or released; it receives the new value. |
| `foregroundColor` | `Color` | `Color.RED` | The color while pressed. |
| `backgroundColor` | `Color` | `Color.BLACK` | The color behind the button. |
| `outlineColor` | `Color` | `Color.CLEAR` | The outline color. |
| `thickness` | `int` | `3` | The outline thickness, in pixels. |
| `rotation` | `int or float` | `0` | How far to turn the button, in degrees, counter-clockwise. |
| `visibility` | `int` | `100` | How visible the button is, from 0 (invisible) to 100 (fully visible). |

For example,

```python title="simplePush.py"
--8<-- "examples/_snippets/simplePush.py"
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Push `push` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`push.getValue()`](getValue.md) | Report whether the object is currently held down. |
| [`push.setValue(newValue)`](setValue.md) | Set whether the object is pressed. |

### Position

| Function | Description |
|---|---|
| [`push.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`push.getX()`](getX.md) | Return the object's horizontal position. |
| [`push.getY()`](getY.md) | Return the object's vertical position. |
| [`push.getCenter()`](getCenter.md) | Return the object's center point. |
| [`push.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`push.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`push.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`push.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`push.setY(y)`](setY.md) | Set the object's vertical position. |
| [`push.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`push.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`push.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`push.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`push.getSize()`](getSize.md) | Return the object's width and height. |
| [`push.getWidth()`](getWidth.md) | Return the object's width. |
| [`push.getHeight()`](getHeight.md) | Return the object's height. |
| [`push.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`push.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`push.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`push.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`push.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`push.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`push.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`push.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Information

| Function | Description |
|---|---|
| [`push.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`push.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`push.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`push.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`push.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`push.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`push.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`push.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`push.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`push.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse push is pressed on this object. |
| [`push.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse push is released over this object. |
| [`push.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`push.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`push.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`push.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`push.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`push.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`push.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
