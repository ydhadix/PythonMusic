# HFader

Create a horizontal fader the user can drag left and right.

Faders are drawn between a starting point (x1, y1) and an ending point (x2, y2).

There are two types of faders, a horizontal fader (HFader) and a [vertical fader (VFader)](../vfader/index.md).

## Creating an HFader

You can create an HFader using the following functions:

```python
HFader(x1, y1, x2, y2)
```

```python
HFader(x1, y1, x2, y2, minValue, maxValue, startValue, action, foregroundColor, backgroundColor, outlineColor, thickness, rotation, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x1` | `int or float` | _required_ | The horizontal position of the top-left corner, in pixels. |
| `y1` | `int or float` | _required_ | The vertical position of the top-left corner, in pixels. |
| `x2` | `int or float` | _required_ | The horizontal position of the bottom-right corner, in pixels. |
| `y2` | `int or float` | _required_ | The vertical position of the bottom-right corner, in pixels. |
| `minValue` | `int` | `0` | The smallest value the fader can take. |
| `maxValue` | `int` | `999` | The largest value the fader can take. |
| `startValue` | `int or float` | `None` | The fader's starting value. Defaults to halfway between minValue and maxValue. |
| `action` | `function` | `None` | The function to call when the fader moves; it receives the new value. |
| `foregroundColor` | `Color` | `Color.RED` | The color of the filled level. |
| `backgroundColor` | `Color` | `Color.BLACK` | The color behind the level. |
| `outlineColor` | `Color` | `Color.BLACK` | The outline color. |
| `thickness` | `int` | `3` | The outline thickness, in pixels. |
| `rotation` | `int or float` | `0` | How far to turn the fader, in degrees, counter-clockwise. |
| `visibility` | `int` | `100` | How visible the fader is, from 0 (invisible) to 100 (fully visible). |

For example, 

```python title="simpleFader.py"
--8<-- "examples/_snippets/simpleFader.py"
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a HFader `hfader` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`hfader.setValue(newValue)`](setValue.md) | Set the object's value. |
| [`hfader.getValue()`](getValue.md) | Return the object's current value. |

### Position

| Function | Description |
|---|---|
| [`hfader.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`hfader.getX()`](getX.md) | Return the object's horizontal position. |
| [`hfader.getY()`](getY.md) | Return the object's vertical position. |
| [`hfader.getCenter()`](getCenter.md) | Return the object's center point. |
| [`hfader.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`hfader.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`hfader.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`hfader.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`hfader.setY(y)`](setY.md) | Set the object's vertical position. |
| [`hfader.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`hfader.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`hfader.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`hfader.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`hfader.getSize()`](getSize.md) | Return the object's width and height. |
| [`hfader.getWidth()`](getWidth.md) | Return the object's width. |
| [`hfader.getHeight()`](getHeight.md) | Return the object's height. |
| [`hfader.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`hfader.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`hfader.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`hfader.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`hfader.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`hfader.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`hfader.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`hfader.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Information

| Function | Description |
|---|---|
| [`hfader.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`hfader.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`hfader.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`hfader.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`hfader.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`hfader.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`hfader.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`hfader.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`hfader.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`hfader.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse hfader is pressed on this object. |
| [`hfader.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse hfader is released over this object. |
| [`hfader.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`hfader.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`hfader.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`hfader.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`hfader.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`hfader.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`hfader.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
