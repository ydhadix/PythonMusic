# addOrder()

Add a GUI object to the display at the given position and layer.

```python
display.addOrder(item, order)
```

Same as [add()](add.md), but also sets the object's layer. Layers run from smallest to largest, where 0 is closest to the front. If the object is already on another display, it is removed from there first.

## Parameters

```python
display.addOrder(item, order, x=None, y=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item` | `Drawable` | _required_ | The GUI object to add. |
| `order` | `int` | _required_ | The layer to place the object on; 0 is closest to the front. |
| `x` | `int or float` | `None` | The horizontal position, in pixels. Defaults to the object's current position. |
| `y` | `int or float` | `None` | The vertical position, in pixels. Defaults to the object's current position. |
