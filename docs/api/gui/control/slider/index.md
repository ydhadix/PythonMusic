# Slider

Create a slider the user can drag to choose a value.

## Creating a Slider

You can create a Slider using the following functions:

```python
Slider()
```

```python
Slider(orientation, minValue, maxValue, startValue, action)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `orientation` | `int` | `HORIZONTAL` | The slider direction, either `HORIZONTAL` or `VERTICAL`. |
| `minValue` | `int` | `0` | The smallest value the slider can take. |
| `maxValue` | `int` | `100` | The largest value the slider can take. |
| `startValue` | `int or float` | `None` | The slider's starting value. Defaults to halfway between `minValue` and `maxValue`. |
| `action` | `function` | `None` | The function to call when the slider moves; it receives one parameter, the new value. |

For example,

```python
slider = Slider(VERTICAL, 0, 127, 50, changeVolume)
```

where `changeVolume` is a function which expects one parameter, the new value of the slider. When the function is called, it may use this value to update the volume of some musical material, for instance.

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Slider `slider` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`slider.getValue()`](getValue.md) | Return the object's current value. |
| [`slider.setValue(value)`](setValue.md) | Set the object's value. |

### Position

| Function | Description |
|---|---|
| [`button.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`button.getX()`](getX.md) | Return the object's horizontal position. |
| [`button.getY()`](getY.md) | Return the object's vertical position. |
| [`button.getCenter()`](getCenter.md) | Return the object's center point. |
| [`button.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`button.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`button.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`button.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`button.setY(y)`](setY.md) | Set the object's vertical position. |
| [`button.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`button.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`button.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`button.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`button.getSize()`](getSize.md) | Return the object's width and height. |
| [`button.getWidth()`](getWidth.md) | Return the object's width. |
| [`button.getHeight()`](getHeight.md) | Return the object's height. |
| [`button.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`button.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`button.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

**NOTE:** Controls cannot be rotated.  A control has these methods available, but they do nothing.

| Function | Description |
|---|---|
| [`button.setRotation(rotation)`](setRotation.md) | Do nothing, since controls cannot be turned. |
| [`button.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`button.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`button.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`button.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Information

| Function | Description |
|---|---|
| [`button.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`button.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`button.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`button.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`button.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`button.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`button.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`button.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`button.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`button.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`button.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`button.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`button.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`button.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`button.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`button.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`button.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`button.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
