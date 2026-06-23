# setOrder()

Move an object to a different layer within the group.

```python
xypad.setOrder(item, order)
```

Layers run from smallest to largest, where 0 is closest to the front. Does nothing if the object is not in the group.

## Parameters

```python
xypad.setOrder(item, order)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item` | `Drawable` | _required_ | The object to re-layer. |
| `order` | `int` | _required_ | The layer to move it to; 0 is closest to the front. |
