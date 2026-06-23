# setOrder()

Move an object to a different layer within the collection.

Layers run from smallest to largest, where 0 is closest to the front. Does nothing if the object is not in the collection.

## Parameters

Once an object `collection` has been created, you can use the following function:

```python
collection.setOrder(item, order)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item` | `Drawable` | _required_ | The object to re-layer. |
| `order` | `int` | _required_ | The layer to move it to; 0 is closest to the front. |
