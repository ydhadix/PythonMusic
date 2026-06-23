# CheckBox

Create a checkbox the user can check and uncheck.

## Creating a CheckBox

You can create a CheckBox using the following functions:

```python
CheckBox()
```

```python
CheckBox(text, action, color)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | `''` | The text shown beside the checkbox. |
| `action` | `function` | `None` | The function to call when the checkbox changes; it receives one parameter, True if it was just checked or False if it was just unchecked. |
| `color` | `Color` | `Color.CLEAR` | The checkbox color. |

For example,

```python
checkbox = Checkbox("Check Me Out!")
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a CheckBox `checkbox` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`checkbox.getText()`](getText.md) | Return the object's text. |
| [`checkbox.setText(text)`](setText.md) | Set the object's text. |
| [`checkbox.setColor(color)`](setColor.md) | Set the object's color. |

### Checking State

If you create a CheckBox without a callback function, it is a passive GUI element.  You can still check whether the CheckBox is checked or unchecked using these functions:

| Function | Description |
|---|---|
| [`checkbox.check()`](check.md) | Check the checkbox. |
| [`checkbox.uncheck()`](uncheck.md) | Uncheck the checkbox. |
| [`checkbox.isChecked()`](isChecked.md) | Report whether the checkbox is checked. |

### Position

| Function | Description |
|---|---|
| [`checkbox.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`checkbox.getX()`](getX.md) | Return the object's horizontal position. |
| [`checkbox.getY()`](getY.md) | Return the object's vertical position. |
| [`checkbox.getCenter()`](getCenter.md) | Return the object's center point. |
| [`checkbox.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`checkbox.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`checkbox.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`checkbox.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`checkbox.setY(y)`](setY.md) | Set the object's vertical position. |
| [`checkbox.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`checkbox.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`checkbox.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`checkbox.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`checkbox.getSize()`](getSize.md) | Return the object's width and height. |
| [`checkbox.getWidth()`](getWidth.md) | Return the object's width. |
| [`checkbox.getHeight()`](getHeight.md) | Return the object's height. |
| [`checkbox.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`checkbox.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`checkbox.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

**NOTE:** Controls cannot be rotated.  Controls have these functions available, but they do nothing.

| Function | Description |
|---|---|
| [`checkbox.setRotation(rotation)`](setRotation.md) | Do nothing, since controls cannot be turned. |
| [`checkbox.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`checkbox.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`checkbox.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`checkbox.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Information

| Function | Description |
|---|---|
| [`checkbox.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`checkbox.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`checkbox.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`checkbox.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`checkbox.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`checkbox.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`checkbox.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`checkbox.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`checkbox.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`checkbox.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse checkbox is pressed on this object. |
| [`checkbox.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse checkbox is released over this object. |
| [`checkbox.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`checkbox.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`checkbox.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`checkbox.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`checkbox.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`checkbox.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`checkbox.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
