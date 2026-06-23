# TextField

Create a single-line text field the user can type into.

If you create a TextField with a callback function, then that function will be called anytime the enter key is typed inside the box. (Presumably, the user will change the text and then press enter.)

## Creating a TextField

You can create a TextField using the following functions:

```python
TextField()
```

```python
TextField(text, columns, action, color, font)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | `''` | The text to start with. |
| `columns` | `int` | `8` | The width of the field, in characters. |
| `action` | `function` | `None` | The function to call when the user presses Enter in the field; it receives one parameter, the field's contents as a string. |
| `color` | `Color` | `Color.WHITE` | The field color. |
| `font` | `Font` | `None` | The font, for example `Font("Serif", Font.ITALIC, 16)`. If omitted, the default font is used. |

For example,

```python
textfield = TextField("type and hit <ENTER> ", 18, processEntry)
```

where `processEntry` is a function which expects one parameter, the updated text (a string).

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a TextField `textfield` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`textfield.getFont()`](getFont.md) | Return the field's font. |
| [`textfield.setFont(font)`](setFont.md) | Set the field's font. |
| [`textfield.setColor(color)`](setColor.md) | Set the field's background color. |

### Checking State

If you create a TextField without a callback function, it is a passive GUI element.  You can still check the text in the TextField using these functions:

| Function | Description |
|---|---|
| [`textfield.getText()`](getText.md) | Return the text in the field. |
| [`textfield.setText(text)`](setText.md) | Set the text in the field. |

### Position

| Function | Description |
|---|---|
| [`textfield.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`textfield.getX()`](getX.md) | Return the object's horizontal position. |
| [`textfield.getY()`](getY.md) | Return the object's vertical position. |
| [`textfield.getCenter()`](getCenter.md) | Return the object's center point. |
| [`textfield.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`textfield.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`textfield.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`textfield.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`textfield.setY(y)`](setY.md) | Set the object's vertical position. |
| [`textfield.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`textfield.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`textfield.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`textfield.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`textfield.getSize()`](getSize.md) | Return the object's width and height. |
| [`textfield.getWidth()`](getWidth.md) | Return the object's width. |
| [`textfield.getHeight()`](getHeight.md) | Return the object's height. |
| [`textfield.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`textfield.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`textfield.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

**NOTE:** Controls cannot be rotated.  A control has these methods available, but they do nothing.

| Function | Description |
|---|---|
| [`textfield.setRotation(rotation)`](setRotation.md) | Do nothing, since controls cannot be turned. |
| [`textfield.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`textfield.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`textfield.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`textfield.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Information

| Function | Description |
|---|---|
| [`textfield.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`textfield.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`textfield.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`textfield.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`textfield.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`textfield.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`textfield.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`textfield.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`textfield.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`textfield.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse textfield is pressed on this object. |
| [`textfield.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse textfield is released over this object. |
| [`textfield.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`textfield.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`textfield.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`textfield.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`textfield.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`textfield.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`textfield.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
