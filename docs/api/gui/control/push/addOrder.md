# addOrder()

Add an object to the group on a given layer.

```python
push.addOrder(item)
```

Same as [add()](add.md), but also sets the object's layer within the group. Layers run from smallest to largest, where 0 is closest to the front.

## Parameters

```python
push.addOrder(item, order=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item` | `Drawable` | _required_ | The object to add. |
| `order` | `int` | `0` | The layer to place it on; 0 is closest to the front. |
