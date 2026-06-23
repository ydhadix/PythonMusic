# onMouseDrag()

Register a function to call when the mouse is dragged (moved while a button is held down) over this object.

## Parameters

Once an object `item` has been created, you can use the following function:

```python
item.onMouseDrag(action)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `action` | `function` | _required_ | The function to call; it receives two parameters, x and y, giving the mouse position in display coordinates. |
