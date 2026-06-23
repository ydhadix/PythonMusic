# Button

Create a clickable button that can be pressed by the user.

Pressing a Button calls a function, specified when the button is created.

## Creating a Button

You can create a Button using the following functions:

```python
Button()
```

```python
Button(text, action, color)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | `''` | The text shown on the button. |
| `action` | `function` | `None` | The function to call each time the button is pressed; it receives no parameters. |
| `color` | `Color` | `Color.LIGHT_GRAY` | The button color. |

For example,

```python
button = Button("Play music", playMusic)
```

where `playMusic` is a function with zero parameters.  This function will be called automatically when the user presses this button.

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Button `button` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`button.getText()`](getText.md) | Return the object's text. |
| [`button.setText(text)`](setText.md) | Set the object's text. |
| [`button.setColor(color)`](setColor.md) | Set the object's color. |

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