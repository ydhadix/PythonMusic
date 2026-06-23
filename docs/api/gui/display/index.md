# Display

A Display is the window your GUI objects appear in. Build a GUI by adding shapes, images, text, and controls to it with [add()](add.md). The window opens as soon as you create it. Inside the display the origin (0, 0) is the top-left corner; x increases to the right and y increases downward.

A program may have several displays open. Displays may contain any number of GUI objects, but they cannot contain another display.

Once a display has been created, you populate it by placing various GUI widgets and graphics objects on it. The library provides various GUI widgets and graphics objects.

## Creating a Display

You can create a Display using the following functions:

```python
Display()
```

```python
Display(title, width, height, x, y, color)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `str` | `''` | The window title. |
| `width` | `int or float` | `600` | The window width, in pixels. |
| `height` | `int or float` | `400` | The window height, in pixels. |
| `x` | `int or float` | `0` | The horizontal position of the window's top-left corner on the screen, in pixels. |
| `y` | `int or float` | `50` | The vertical position of the window's top-left corner on the screen, in pixels. |
| `color` | `Color` | `Color.WHITE` | The background color. |

For example,

```python
display = Display("Simple GUI", 120, 60)
```

## Functions

Once a Display `display` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`display.add(item)`](add.md) | Add a GUI object to the display at the given position. |
| [`display.remove(item)`](remove.md) | Remove a GUI object from the display. |
| [`display.removeAll()`](removeAll.md) | Remove every GUI object from the display. |
| [`display.move(item, x, y)`](move.md) | Move a GUI object to a new position on the display. |
| [`display.getItems()`](getItems.md) | Return the GUI objects currently on the display. |

### Layering GUI Objects

GUI objects on a Display are layered.  Typically, the most recent object sits on top of the others (`order = 0`).  You can change the order 

| Function | Description |
|---|---|
| [`display.addOrder(item)`](add.md) | Add a GUI object to the display at the given position and layer. |
| [`display.getOrder(item)`](getOrder.md) | Return the layer a GUI object sits on. |
| [`display.setOrder(item, order)`](setOrder.md) | Move a GUI object to a different layer. |

### Adding Menus

[Menu](../control/menu/index.md) objects are different from other objects; instead of appearing on a Display, menu objects are added to the Display's menu bar, or as context (right click, pop-up) menus.

| Function | Description |
|---|---|
| [`display.addMenu(menu)`](addMenu.md) | Add a menu to the display's menu bar. |
| [`display.addPopupMenu(menu)`](addPopupMenu.md) | Add a pop-up (right-click) menu to the display. |

### Manipulating the Display

These functions are useful for updating how a Display appears on the screen.

| Function | Description |
|---|---|
| [`display.getTitle()`](getTitle.md) | Return the display's title. |
| [`display.getSize()`](getSize.md) | Return the display's width and height. |
| [`display.getWidth()`](getWidth.md) | Return the display's width. |
| [`display.getHeight()`](getHeight.md) | Return the display's height. |
| [`display.getPosition()`](getPosition.md) | Return the display's position on the screen. |
| [`display.getColor()`](getColor.md) | Return the display's background color. |
| [`display.setTitle(title)`](setTitle.md) | Set the display's title. |
| [`display.setSize(width, height)`](setSize.md) | Set the display's width and height. |
| [`display.setWidth(width)`](setWidth.md) | Set the display's width. |
| [`display.setHeight(height)`](setHeight.md) | Set the display's height. |
| [`display.setPosition(x, y)`](setPosition.md) | Set the display's position on the screen. |
| [`display.setColor()`](setColor.md) | Set the display's background color. |
| [`display.show()`](show.md) | Show the display. |
| [`display.hide()`](hide.md) | Hide the display. |
| [`display.close()`](close.md) | Close the display. |
| [`display.save(filename)`](save.md) | Save a picture of the display to an image file. |
| [`display.setToolTipText()`](setToolTipText.md) | Set the hover text shown over the display. |
| [`display.showMouseCoordinates()`](showMouseCoordinates.md) | Show the mouse position in the display's tooltip as the mouse moves. |
| [`display.hideMouseCoordinates()`](hideMouseCoordinates.md) | Stop showing the mouse position in the display's tooltip. |

### Drawing Shapes

In addition to adding movable GUI objects to a Display, you can also draw shapes and text directly to the Display's background.  Drawing shapes is faster than adding GUI objects, but drawn shapes can't be moved or erased without clearing the entire canvas (using [clearDrawing()](clearDrawing.md)).

| Function | Description |
|---|---|
| [`display.drawRectangle(x1, y1, x2, y2)`](drawRectangle.md) | Draw a rectangle straight onto the display. |
| [`display.drawOval(x1, y1, x2, y2)`](drawOval.md) | Draw an oval straight onto the display. |
| [`display.drawCircle(x, y, radius)`](drawCircle.md) | Draw a circle straight onto the display. |
| [`display.drawPoint(x, y)`](drawPoint.md) | Draw a single point straight onto the display. |
| [`display.drawArc(x1, y1, x2, y2)`](drawArc.md) | Draw an arc straight onto the display. |
| [`display.drawArcCircle(x, y, radius)`](drawArcCircle.md) | Draw a circular arc straight onto the display. |
| [`display.drawPolyline(xPoints, yPoints)`](drawPolyline.md) | Draw a connected series of line segments straight onto the display. |
| [`display.drawLine(x1, y1, x2, y2)`](drawLine.md) | Draw a line straight onto the display. |
| [`display.drawPolygon(xPoints, yPoints)`](drawPolygon.md) | Draw a polygon straight onto the display. |
| [`display.drawIcon(filename, x, y)`](drawIcon.md) | Draw an image straight onto the display. |
| [`display.drawLabel(text, x, y)`](drawLabel.md) | Draw a line of text straight onto the display. |
| [`display.drawText(text, x, y)`](drawText.md) | Draw a line of text straight onto the display. |
| [`display.clearDrawing()`](clearDrawing.md) | Erase everything drawn with the draw… methods. |

### Events

Displays have the same [event functions](../event/index.md) as other GUI objects, plus their own [onClose()](onClose.md) event.

| Function | Description |
|---|---|
| [`display.onClose(action)`](onClose.md) | Set up a function to call right before the display closes. |
| [`display.onMouseClick(action)`](onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`display.onMouseDown(action)`](onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`display.onMouseUp(action)`](onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`display.onMouseMove(action)`](onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`display.onMouseDrag(action)`](onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |
| [`display.onMouseEnter(action)`](onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`display.onMouseExit(action)`](onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
| [`display.onKeyType(action)`](onKeyType.md) | Set up a function to call when a key is typed (pressed and released). |
| [`display.onKeyDown(action)`](onKeyDown.md) | Set up a function to call when a key is pressed down. |
| [`display.onKeyUp(action)`](onKeyUp.md) | Set up a function to call when a key is released. |
