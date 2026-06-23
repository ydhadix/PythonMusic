# Label

Create a label that shows a line of text.

## Creating a Label

You can create a Label using the following functions:

```python
Label(text)
```

```python
Label(text, alignment, textColor, backgroundColor, font, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | _required_ | The text to show. |
| `alignment` | `int` | `LEFT` | How the text lines up, one of `LEFT`, `CENTER`, or `RIGHT`. |
| `textColor` | `Color` | `Color.BLACK` | The text color. |
| `backgroundColor` | `Color` | `Color.CLEAR` | The color behind the text. Defaults to transparent. |
| `font` | `Font` | `None` | The font, for example `Font("Serif", Font.ITALIC, 16)`. If omitted, the system default font is used. |
| `visibility` | `int` | `100` | How visible the label is, from 0 (invisible) to 100 (fully visible). |

For example,

```python
label = Label("Hello World!")
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a Label `label` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`label.getText()`](getText.md) | Return the label's text. |
| [`label.getAlignment()`](getAlignment.md) | Return how the label's text lines up. |
| [`label.getFont()`](getFont.md) | Return the label's font. |
| [`label.setText(text)`](setText.md) | Set the label's text. |
| [`label.setAlignment(alignment)`](setAlignment.md) | Set how the label's text lines up. |
| [`label.setFont(font)`](setFont.md) | Set the label's font. |

### Position

| Function | Description |
|---|---|
| [`label.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`label.getX()`](getX.md) | Return the object's horizontal position. |
| [`label.getY()`](getY.md) | Return the object's vertical position. |
| [`label.getCenter()`](getCenter.md) | Return the object's center point. |
| [`label.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`label.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`label.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`label.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`label.setY(y)`](setY.md) | Set the object's vertical position. |
| [`label.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`label.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`label.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`label.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`label.getSize()`](getSize.md) | Return the object's width and height. |
| [`label.getWidth()`](getWidth.md) | Return the object's width. |
| [`label.getHeight()`](getHeight.md) | Return the object's height. |
| [`label.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`label.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`label.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`label.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`label.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`label.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`label.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`label.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Color

| Function | Description |
|---|---|
| [`label.getColor()`](getColor.md) | Return the shape's text color. |
| [`label.getTextColor()`](getTextColor.md) | Return the label's text color. |
| [`label.getBackgroundColor()`](getBackgroundColor.md) | Return the label's background color. |
| [`label.getFill()`](getFill.md) | Report whether the shape is filled in. |
| [`label.getThickness()`](getThickness.md) | Return the shape's outline thickness. |
| [`label.setColor()`](setColor.md) | Set the shape's text color. |
| [`label.setTextColor()`](setTextColor.md) | Set the label's text color. |
| [`label.setBackgroundColor()`](setBackgroundColor.md) | Set the label's background color. |
| [`label.setFill(fill)`](setFill.md) | Set whether the shape is filled in. |
| [`label.setThickness(thickness)`](setThickness.md) | Set the shape's outline thickness. |

### Information

| Function | Description |
|---|---|
| [`label.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`label.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`label.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`label.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`label.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`label.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`label.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`label.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`label.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`label.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse label is pressed on this object. |
| [`label.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse label is released over this object. |
| [`label.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`label.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`label.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`label.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`label.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`label.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`label.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
