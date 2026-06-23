# Mouse Events

The following functions handle various mouse events.

The first group handles mouse events which happen **inside** a GUI object (e.g., [Display](../../display/index.md), [Circle](../../shapes/circle/index.md), etc.):

| Function | Description |
|---|---|
| [`onMouseClick(action)`](../../common/events/mouse/onMouseClick.md) | Register a function to call when the mouse is clicked on this object. |
| [`onMouseDown(action)`](../../common/events/mouse/onMouseDown.md) | Register a function to call when the mouse button is pressed on this object. |
| [`onMouseUp(action)`](../../common/events/mouse/onMouseUp.md) | Register a function to call when the mouse button is released over this object. |
| [`onMouseMove(action)`](../../common/events/mouse/onMouseMove.md) | Register a function to call when the mouse moves over this object. |
| [`onMouseDrag(action)`](../../common/events/mouse/onMouseDrag.md) | Register a function to call when the mouse is dragged over this object. |

The following functions handle movement of mouse that crosses the borders of a GUI object (i.e., entering or exiting the object boundaries):

| Function | Description |
|---|---|
| [`onMouseEnter(action)`](../../common/events/mouse/onMouseEnter.md) | Register a function to call when the mouse moves onto this object. |
| [`onMouseExit(action)`](../../common/events/mouse/onMouseExit.md) | Register a function to call when the mouse moves off this object. |
