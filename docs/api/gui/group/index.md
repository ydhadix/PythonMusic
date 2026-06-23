# Group

Bundle several GUI objects so they move, turn, and scale together.

## Creating a Group

You can create a Group using the following functions:

```python
Group()
```

```python
Group(itemList)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `itemList` | `list[Drawable]` | `[]` | The objects to start the group with. |

For example,

```python
group = Group(itemList)
```

where `itemList` is a list of GUI objects.  Moving, resizing, and rotating the group also changes the items within it accordingly.

Once created, you can add it to a [Display](../display/index.md) using the Display's [add()](../display/add.md) function.

## Functions

Once a Group `group` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`group.add(item)`](add.md) | Add an object to the group. |
| [`group.addOrder(item)`](addOrder.md) | Add an object to the group on a given layer. |
| [`group.remove(item)`](remove.md) | Remove an object from the group. |
| [`group.getOrder(item)`](getOrder.md) | Return the layer an object sits on within the group. |
| [`group.setOrder(item, order)`](setOrder.md) | Move an object to a different layer within the group. |
| [`group.getItems()`](getItems.md) | Return the objects currently in the group. |

### Position

| Function | Description |
|---|---|
| [`group.getPosition()`](getPosition.md) | Return the object's position, the top-left corner of its bounding box. |
| [`group.getX()`](getX.md) | Return the object's horizontal position. |
| [`group.getY()`](getY.md) | Return the object's vertical position. |
| [`group.getCenter()`](getCenter.md) | Return the object's center point. |
| [`group.getCenterX()`](getCenterX.md) | Return the object's horizontal center. |
| [`group.getCenterY()`](getCenterY.md) | Return the object's vertical center. |
| [`group.setPosition(x, y)`](setPosition.md) | Move the object so the top-left corner of its bounding box sits at the given point. |
| [`group.setX(x)`](setX.md) | Set the object's horizontal position. |
| [`group.setY(y)`](setY.md) | Set the object's vertical position. |
| [`group.setCenter(x, y)`](setCenter.md) | Move the object so its center sits at the given point. |
| [`group.setCenterX(x)`](setCenterX.md) | Set the object's horizontal center. |
| [`group.setCenterY(y)`](setCenterY.md) | Set the object's vertical center. |
| [`group.move(x, y)`](move.md) | Move the object to a new position. |

### Size

| Function | Description |
|---|---|
| [`group.getSize()`](getSize.md) | Return the object's width and height. |
| [`group.getWidth()`](getWidth.md) | Return the object's width. |
| [`group.getHeight()`](getHeight.md) | Return the object's height. |
| [`group.setSize(width, height)`](setSize.md) | Set the object's width and height. |
| [`group.setWidth(width)`](setWidth.md) | Set the object's width. |
| [`group.setHeight(height)`](setHeight.md) | Set the object's height. |

### Rotation

| Function | Description |
|---|---|
| [`group.getRotation()`](getRotation.md) | Return how far the object is turned. |
| [`group.setRotation(rotation)`](setRotation.md) | Turn the object to a given angle. |
| [`group.rotate(angle)`](rotate.md) | Turn the object by an additional angle. |

### Visibility

| Function | Description |
|---|---|
| [`group.getVisibility()`](getVisibility.md) | Return how visible the object is. |
| [`group.setVisibility(visibility)`](setVisibility.md) | Set how visible the object is. |

### Information

| Function | Description |
|---|---|
| [`group.getEndpoints()`](getEndpoints.md) | Return the object's four corners. |
| [`group.getBoundingBox()`](getBoundingBox.md) | Return the smallest upright box that surrounds the object. |
| [`group.getGroup()`](getGroup.md) | Return the Group this object belongs to. |
| [`group.getDisplay()`](getDisplay.md) | Return the Display this object is on. |
| [`group.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the object. |

### Hit Testing

| Function | Description |
|---|---|
| [`group.contains(x, y)`](contains.md) | Report whether a point lies inside the object. |
| [`group.intersects(other)`](intersects.md) | Report whether this object overlaps another. |
| [`group.encloses(other)`](encloses.md) | Report whether this object completely contains another. |

### Events

| Function | Description |
|---|---|
| [`group.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`group.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse group is pressed on this object. |
| [`group.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse group is released over this object. |
| [`group.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`group.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`group.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`group.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`group.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`group.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`group.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
