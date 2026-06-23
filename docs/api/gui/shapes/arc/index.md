# Arc

Create an arc, part of an oval that fills the box given by two opposite corners.

Arcs are drawn between a starting point (x1, y1) and an ending point (x2, y2).  They look like [Ovals](../oval/index.md), except only the section from `startAngle` to `endAngle` is visible.

## Creating an Arc

You can create an Arc using the following functions:

```python
Arc(x1, y1, x2, y2)
```

```python
Arc(x1, y1, x2, y2, startAngle, endAngle, style, color, fill, thickness, rotation, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x1` | `int or float` | _required_ | The horizontal position of the box's top-left corner, in pixels. |
| `y1` | `int or float` | _required_ | The vertical position of the box's top-left corner, in pixels. |
| `x2` | `int or float` | _required_ | The horizontal position of the box's bottom-right corner, in pixels. |
| `y2` | `int or float` | _required_ | The vertical position of the box's bottom-right corner, in pixels. |
| `startAngle` | `int or float` | `PI` | The starting angle, in degrees. |
| `endAngle` | `int or float` | `TWO_PI` | The ending angle, in degrees. |
| `style` | `int` | `OPEN` | The arc style, one of OPEN (an open arc), CHORD (closed with a straight line between the ends), or PIE (closed with two lines to the center). |
| `color` | `Color` | `Color.BLACK` | The color. |
| `fill` | `bool` | `False` | Whether the arc is filled in (True) or just an outline (False). |
| `thickness` | `int` | `1` | The outline thickness, in pixels. |
| `rotation` | `int or float` | `0` | How far to turn the arc, in degrees, counter-clockwise. |
| `visibility` | `int` | `100` | How visible the arc is, from 0 (invisible) to 100 (fully visible). |

For example,

```python
arc = Arc(100, 100, 200, 200, 0, 180)
```

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once an Arc `arc` has been created, the following functions are available:

### Position

| Function | Description |
|---|---|
| [`arc.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`arc.getX()`](getX.md) | Return the object's horizontal position. |
| [`arc.getY()`](getY.md) | Return the object's vertical position. |
| [`arc.getCenter()`](getCenter.md) | Return the object's center point. |
| [`arc.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`arc.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`arc.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`arc.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`arc.setY(y)`](setY.md) | Set the object's vertical position. |
| [`arc.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`arc.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`arc.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`arc.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`arc.getSize()`](getSize.md) | Return the object's width and height. |
| [`arc.getWidth()`](getWidth.md) | Return the object's width. |
| [`arc.getHeight()`](getHeight.md) | Return the object's height. |
| [`arc.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`arc.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`arc.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`arc.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`arc.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`arc.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`arc.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`arc.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Color

| Function | Description |
|---|---|
| [`arc.getColor()`](getColor.md) | Return the shape's color. |
| [`arc.getFill()`](getFill.md) | Report whether the shape is filled in. |
| [`arc.getThickness()`](getThickness.md) | Return the shape's outline thickness. |
| [`arc.setColor()`](setColor.md) | Set the shape's color. |
| [`arc.setFill(fill)`](setFill.md) | Set whether the shape is filled in. |
| [`arc.setThickness(thickness)`](setThickness.md) | Set the shape's outline thickness. |

### Information

| Function | Description |
|---|---|
| [`arc.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`arc.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`arc.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`arc.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`arc.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`arc.contains(x, y)`](contains.md) | Report whether a point lies on (or inside) the arc. |
| [`arc.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`arc.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`arc.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`arc.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`arc.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`arc.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`arc.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`arc.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`arc.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`arc.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`arc.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`arc.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
