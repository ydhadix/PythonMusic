# Events

Every GUI object listens for mouse clicks, mouse drags, typing a key, etc. This allows you to specify a callback function.

*Callback functions* are functions to be called when a user action occurs.

You do not have to specify a callback function for everything – only for what you want. For example, you can have a display, which – when clicked – a circle is drawn, and – when spacebar is pressed – all circles are removed.

**Note:**
- If two objects are overlapping, events are handled by the object on top.
- When an object receives an event, the Display that object is on also receives that event.  If the object and Display both have callback functions, the Display's callback is called last.

The following mouse and keyboard event functions are available for **all** GUI library objects (except Menus):

| Contents | Description |
|---|---|
| [Mouse Events](mouse/index.md) | Events for responding to mouse movement and button presses. |
| [Keyboard Events](keyboard/index.md) | Events for responding to keyboard presses. |
| [Display Events](display/index.md) | Events only for Displays. |
