# TextArea

Create a multi-line text area the user can type into.

TextArea objects are used for entering text that may span several lines.  If the text is taller than the area, a scroll bar appears on the right.

## Creating a TextArea

You can create a TextArea using the following functions:

```python
TextArea()
```

```python
TextArea(text, columns, rows, color, font)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | `''` | The text to start with. |
| `columns` | `int` | `8` | The width of the area, in characters. |
| `rows` | `int` | `5` | The height of the area, in lines. |
| `color` | `Color` | `Color.WHITE` | The area color. |
| `font` | `Font` | `None` | The font, for example `Font("Serif", Font.ITALIC, 16)`. If omitted, the default font is used. |

For example,

```python
textarea = TextArea("Start Typing...", 10, 8, Color.YELLOW)
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a TextArea `textarea` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`textarea.getText()`](getText.md) | Return the text in the area. |
| [`textarea.getFont()`](getFont.md) | Return the area's font. |
| [`textarea.setText(text)`](setText.md) | Set the text in the area. |
| [`textarea.setFont(font)`](setFont.md) | Set the area's font. |
| [`textarea.setColor(color)`](setColor.md) | Set the area's color. |

### Position

| Function | Description |
|---|---|
| [`textarea.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`textarea.getX()`](getX.md) | Return the object's horizontal position. |
| [`textarea.getY()`](getY.md) | Return the object's vertical position. |
| [`textarea.getCenter()`](getCenter.md) | Return the object's center point. |
| [`textarea.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`textarea.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`textarea.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`textarea.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`textarea.setY(y)`](setY.md) | Set the object's vertical position. |
| [`textarea.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`textarea.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`textarea.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`textarea.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`textarea.getSize()`](getSize.md) | Return the object's width and height. |
| [`textarea.getWidth()`](getWidth.md) | Return the object's width. |
| [`textarea.getHeight()`](getHeight.md) | Return the object's height. |
| [`textarea.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`textarea.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`textarea.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

**NOTE:** Controls cannot be rotated.  A control has these methods available, but they do nothing.

| Function | Description |
|---|---|
| [`textarea.setRotation(rotation)`](setRotation.md) | Do nothing, since controls cannot be turned. |
| [`textarea.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`textarea.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`textarea.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`textarea.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Information

| Function | Description |
|---|---|
| [`textarea.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`textarea.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`textarea.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`textarea.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`textarea.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`textarea.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`textarea.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`textarea.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`textarea.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`textarea.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse textarea is pressed on this object. |
| [`textarea.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse textarea is released over this object. |
| [`textarea.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`textarea.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`textarea.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`textarea.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`textarea.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`textarea.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`textarea.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
