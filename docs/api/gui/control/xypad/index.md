# XYPad

An XYPad is similar to a trackpad. It is controlled by clicking and dragging a selector (tracker bubble) across the pad.

XYPads are drawn between a starting point (x1, y1) and an ending point (x2, y2).  Its value is an (x, y) position within the pad.

## Creating an XYPad

You can create an XYPad using the following functions:

```python
xypad = XYPad(x1, y1, x2, y2)
```

```python
XYPad(x1, y1, x2, y2, action, foregroundColor, backgroundColor, outlineColor, outlineThickness, trackerRadius, crosshairThickness, rotation, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x1` | `int or float` | _required_ | The horizontal position of the top-left corner, in pixels. |
| `y1` | `int or float` | _required_ | The vertical position of the top-left corner, in pixels. |
| `x2` | `int or float` | _required_ | The horizontal position of the bottom-right corner, in pixels. |
| `y2` | `int or float` | _required_ | The vertical position of the bottom-right corner, in pixels. |
| `action` | `function` | `None` | The function to call when the tracker moves; it receives the new [x, y] value. |
| `foregroundColor` | `Color` | `Color.RED` | The color of the tracker. |
| `backgroundColor` | `Color` | `Color.BLACK` | The color behind the tracker. |
| `outlineColor` | `Color` | `Color.CLEAR` | The outline color. |
| `outlineThickness` | `int` | `2` | The outline thickness, in pixels. |
| `trackerRadius` | `int or float` | `10` | The radius of the tracker, in pixels. |
| `crosshairThickness` | `int` | `None` | The thickness of the crosshair lines, in pixels. Defaults to the outline thickness. |
| `rotation` | `int or float` | `0` | How far to turn the pad, in degrees, counter-clockwise. |
| `visibility` | `int` | `100` | How visible the pad is, from 0 (invisible) to 100 (fully visible). |

For example,

```python title="simpleXYPad.py"
--8<-- "examples/_snippets/simpleXYPad.py"
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once an XYPad `xypad` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`xypad.getValue()`](getValue.md) | Return the tracker's position within the pad. |
| [`xypad.setValue(x, y)`](setValue.md) | Set the tracker's position within the pad. |

### Position

| Function | Description |
|---|---|
| [`xypad.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`xypad.getX()`](getX.md) | Return the object's horizontal position. |
| [`xypad.getY()`](getY.md) | Return the object's vertical position. |
| [`xypad.getCenter()`](getCenter.md) | Return the object's center point. |
| [`xypad.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`xypad.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`xypad.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`xypad.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`xypad.setY(y)`](setY.md) | Set the object's vertical position. |
| [`xypad.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`xypad.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`xypad.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`xypad.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`xypad.getSize()`](getSize.md) | Return the object's width and height. |
| [`xypad.getWidth()`](getWidth.md) | Return the object's width. |
| [`xypad.getHeight()`](getHeight.md) | Return the object's height. |
| [`xypad.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`xypad.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`xypad.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`xypad.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`xypad.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`xypad.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`xypad.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`xypad.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Information

| Function | Description |
|---|---|
| [`xypad.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`xypad.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`xypad.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`xypad.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`xypad.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`xypad.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`xypad.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`xypad.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`xypad.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`xypad.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse xypad is pressed on this object. |
| [`xypad.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse xypad is released over this object. |
| [`xypad.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`xypad.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`xypad.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`xypad.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`xypad.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`xypad.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`xypad.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
