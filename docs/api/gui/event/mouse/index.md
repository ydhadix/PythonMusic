# Mouse Events

The following functions handle various mouse events.

The first group handles mouse events which happen **inside** a GUI object (e.g., [Display](../../display/index.md), [Circle](../../shapes/circle/index.md), etc.):

| Function | Description |
|---|---|
| [`object.onMouseClick(action)`](../../display/onMouseClick.md) | Set up a function to call when the mouse is clicked on this object. |
| [`object.onMouseDown(action)`](../../display/onMouseDown.md) | Set up a function to call when the mouse button is pressed on this object. |
| [`object.onMouseUp(action)`](../../display/onMouseUp.md) | Set up a function to call when the mouse button is released over this object. |
| [`object.onMouseMove(action)`](../../display/onMouseMove.md) | Set up a function to call when the mouse moves over this object. |
| [`object.onMouseDrag(action)`](../../display/onMouseDrag.md) | Set up a function to call when the mouse is dragged over this object. |

The following functions handle movement of mouse that crosses the borders of a GUI object (i.e., entering or exiting the object boundaries):

| Function | Description |
|---|---|
| [`object.onMouseEnter(action)`](../../display/onMouseEnter.md) | Set up a function to call when the mouse moves onto this object. |
| [`object.onMouseExit(action)`](../../display/onMouseExit.md) | Set up a function to call when the mouse moves off this object. |
