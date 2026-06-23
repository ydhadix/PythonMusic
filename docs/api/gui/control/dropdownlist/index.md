# DropDownList

Create a drop-down list the user can pick items from.

## Creating a DropDownList

You can create a DropDownList using the following functions:

```python
dropdown = DropDownList()
```

```python
DropDownList(items, action, color)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `items` | `list[str]` | `[]` | The items to show, for example ["item1", "item2", "item3"]. |
| `action` | `function` | `None` | The function to call when an item is picked; it receives one parameter, the selected item as a string. |
| `color` | `Color` | `Color.LIGHT_GRAY` | The list color. |

For example,

```python
dropdown = DropDownList(["item1", "item2", "item3"], itemSelected)
```

where `itemSelected` is a function which expects one parameter, the selected item (a string).

Once created, you can add it to a [Display](../../display/index.md) using the Display's [add()](../../display/add.md) function.

## Functions

Once a DropDownList `dropdown` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`dropdown.setColor(color)`](setColor.md) | Set the object's color. |

### Position

| Function | Description |
|---|---|
| [`dropdown.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`dropdown.getX()`](getX.md) | Return the object's horizontal position. |
| [`dropdown.getY()`](getY.md) | Return the object's vertical position. |
| [`dropdown.getCenter()`](getCenter.md) | Return the object's center point. |
| [`dropdown.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`dropdown.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`dropdown.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`dropdown.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`dropdown.setY(y)`](setY.md) | Set the object's vertical position. |
| [`dropdown.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`dropdown.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`dropdown.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`dropdown.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`dropdown.getSize()`](getSize.md) | Return the object's width and height. |
| [`dropdown.getWidth()`](getWidth.md) | Return the object's width. |
| [`dropdown.getHeight()`](getHeight.md) | Return the object's height. |
| [`dropdown.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`dropdown.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`dropdown.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

**NOTE:** Controls cannot be rotated.  A control has these methods available, but they do nothing.

| Function | Description |
|---|---|
| [`dropdown.setRotation(rotation)`](setRotation.md) | Do nothing, since controls cannot be turned. |
| [`dropdown.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`dropdown.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`dropdown.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`dropdown.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Information

| Function | Description |
|---|---|
| [`dropdown.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`dropdown.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`dropdown.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`dropdown.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`dropdown.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`dropdown.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`dropdown.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`dropdown.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`dropdown.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`dropdown.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse dropdown is pressed on this object. |
| [`dropdown.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse dropdown is released over this object. |
| [`dropdown.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`dropdown.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`dropdown.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`dropdown.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`dropdown.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`dropdown.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`dropdown.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
