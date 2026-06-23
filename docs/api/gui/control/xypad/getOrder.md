# getOrder()

Return the layer an object sits on within the group.

```python
xypad.getOrder(item)
```

## Parameters

```python
xypad.getOrder(item)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item` | `Drawable` | _required_ | The object to look up. |

## Returns

`return order`

| Value | Type | Description |
|---|---|---|
| order | `int` | The object's layer, where 0 is closest to the front; None if the object is not in the group. |
