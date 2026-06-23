# Rotary

Create a rotary knob the user can turn.

Rotaries are drawn between a starting point (x1, y1) and an ending point (x2, y2). Its lowest and highest values sit at the bottom, and it rotates around `arcWidth` degrees in between.

## Creating a Rotary

You can create a Rotary using the following functions:

```python
Rotary(x1, y1, x2, y2)
```

```python
Rotary(x1, y1, x2, y2, minValue, maxValue, startValue, action, foregroundColor, backgroundColor, outlineColor, thickness, arcWidth, rotation, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x1` | `int or float` | _required_ | The horizontal position of the top-left corner, in pixels. |
| `y1` | `int or float` | _required_ | The vertical position of the top-left corner, in pixels. |
| `x2` | `int or float` | _required_ | The horizontal position of the bottom-right corner, in pixels. |
| `y2` | `int or float` | _required_ | The vertical position of the bottom-right corner, in pixels. |
| `minValue` | `int` | `0` | The smallest value the knob can take. |
| `maxValue` | `int` | `999` | The largest value the knob can take. |
| `startValue` | `int or float` | `None` | The knob's starting value. Defaults to halfway between minValue and maxValue. |
| `action` | `function` | `None` | The function to call when the knob turns; it receives the new value. |
| `foregroundColor` | `Color` | `Color.RED` | The color of the level shown by the knob. |
| `backgroundColor` | `Color` | `Color.BLACK` | The color behind the knob. |
| `outlineColor` | `Color` | `Color.BLUE` | The outline color. |
| `thickness` | `int` | `3` | The outline thickness, in pixels. |
| `arcWidth` | `int or float` | `300` | How far the knob turns from lowest to highest, in degrees. A typical value is 300. |
| `rotation` | `int or float` | `0` | How far to turn the whole control, in degrees, counter-clockwise. |
| `visibility` | `int` | `100` | How visible the knob is, from 0 (invisible) to 100 (fully visible). |

For example,

```python title="simpleRotary.py"
--8<-- "examples/_snippets/simpleRotary.py"
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Rotary `rotary` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`rotary.setValue(newValue)`](setValue.md) | Set the object's value. |
| [`rotary.getValue()`](getValue.md) | Return the object's current value. |

### Position

| Function | Description |
|---|---|
| [`rotary.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`rotary.getX()`](getX.md) | Return the object's horizontal position. |
| [`rotary.getY()`](getY.md) | Return the object's vertical position. |
| [`rotary.getCenter()`](getCenter.md) | Return the object's center point. |
| [`rotary.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`rotary.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`rotary.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`rotary.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`rotary.setY(y)`](setY.md) | Set the object's vertical position. |
| [`rotary.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`rotary.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`rotary.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`rotary.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`rotary.getSize()`](getSize.md) | Return the object's width and height. |
| [`rotary.getWidth()`](getWidth.md) | Return the object's width. |
| [`rotary.getHeight()`](getHeight.md) | Return the object's height. |
| [`rotary.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`rotary.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`rotary.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`rotary.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`rotary.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`rotary.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`rotary.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`rotary.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Information

| Function | Description |
|---|---|
| [`rotary.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`rotary.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`rotary.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`rotary.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`rotary.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`rotary.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`rotary.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`rotary.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`rotary.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`rotary.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse rotary is pressed on this object. |
| [`rotary.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse rotary is released over this object. |
| [`rotary.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`rotary.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`rotary.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`rotary.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`rotary.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`rotary.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`rotary.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
