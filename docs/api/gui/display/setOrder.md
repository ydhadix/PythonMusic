# setOrder()

Move a GUI object to a different layer.

```python
display.setOrder(item, order)
```

Layers run from smallest to largest, where 0 is closest to the front. Does nothing if the object is not on the display.

## Parameters

```python
display.setOrder(item, order)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item` | `Drawable` | _required_ | The GUI object to re-layer. |
| `order` | `int` | _required_ | The layer to move it to; 0 is closest to the front. |
