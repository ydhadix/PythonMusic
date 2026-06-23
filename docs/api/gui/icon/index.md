# Icon

Create an image loaded from a file.

## Creating an Icon

You can create an Icon using the following functions:

```python
Icon(filename)
```

```python
Icon(filename, width, height, rotation, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` | _required_ | The image file to load, ending in ".jpg" or ".png". |
| `width` | `int or float` | `None` | The width to scale the image to, in pixels. Defaults to the image's own width. |
| `height` | `int or float` | `None` | The height to scale the image to, in pixels. Defaults to the image's own height. |
| `rotation` | `int or float` | `0` | How far to turn the image, in degrees, counter-clockwise. |
| `visibility` | `int` | `100` | How visible the image is, from 0 (invisible) to 100 (fully visible). |

For example,

```python
icon = Icon("mona-lisa.jpg")
```

Once created, you can add it to a [Display](../display/index.md) using the Display's [add()](../display/add.md) function.

## Functions

Once an Icon `icon` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`icon.getPixel(column, row)`](getPixel.md) | Return the color of one pixel. |
| [`icon.getPixels()`](getPixels.md) | Return every pixel in the image. |
| [`icon.getColor()`](getColor.md) | Return the last color used with setColor(). |
| [`icon.setPixel(column, row, color)`](setPixel.md) | Set the color of one pixel. |
| [`icon.setPixels(pixels)`](setPixels.md) | Replace every pixel in the image. |
| [`icon.setColor()`](setColor.md) | Sets every pixel to a single color. |
| [`icon.crop(x, y, width, height)`](crop.md) | Crop the image to a rectangular region. |
| [`icon.save(filename)`](save.md) | Save the image to a file. |

### Position

| Function | Description |
|---|---|
| [`icon.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`icon.getX()`](getX.md) | Return the object's horizontal position. |
| [`icon.getY()`](getY.md) | Return the object's vertical position. |
| [`icon.getCenter()`](getCenter.md) | Return the object's center point. |
| [`icon.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`icon.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`icon.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`icon.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`icon.setY(y)`](setY.md) | Set the object's vertical position. |
| [`icon.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`icon.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`icon.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`icon.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`icon.getSize()`](getSize.md) | Return the object's width and height. |
| [`icon.getWidth()`](getWidth.md) | Return the object's width. |
| [`icon.getHeight()`](getHeight.md) | Return the object's height. |
| [`icon.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`icon.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`icon.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`icon.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`icon.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`icon.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`icon.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`icon.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Color

| Function | Description |
|---|---|
| [`icon.getFill()`](getFill.md) | Report whether the shape is filled in. |
| [`icon.getThickness()`](getThickness.md) | Return the shape's outline thickness. |
| [`icon.setFill(fill)`](setFill.md) | Set whether the shape is filled in. |
| [`icon.setThickness(thickness)`](setThickness.md) | Set the shape's outline thickness. |

### Information

| Function | Description |
|---|---|
| [`icon.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`icon.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`icon.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`icon.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`icon.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`icon.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`icon.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`icon.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`icon.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`icon.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`icon.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`icon.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`icon.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`icon.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`icon.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`icon.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`icon.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`icon.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
