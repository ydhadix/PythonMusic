# add()

Add a GUI object to the display at the given position.

```python
display.add(item)
```

Aligns the object's top-left corner (for a Circle, its center) with (x, y), where (0, 0) is the display's top-left corner. An object can be on only one display at a time. Adding it here removes it from any display it was on. If x and y are left out, the object's current position is used.

## Parameters

```python
display.add(item, x=None, y=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item` | `Drawable` | _required_ | The GUI object to add. |
| `x` | `int or float` | `None` | The horizontal position, in pixels. Defaults to the object's current position. |
| `y` | `int or float` | `None` | The vertical position, in pixels. Defaults to the object's current position. |
