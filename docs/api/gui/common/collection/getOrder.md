# getOrder()

Return the layer an object sits on within the collection.

## Parameters

Once an object `collection` has been created, you can use the following function:

```python
collection.getOrder(item)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item` | `Drawable` | _required_ | The object to look up. |

## Returns

`return order`

| Value | Type | Description |
|---|---|---|
| order | `int` | The object's layer, where 0 is closest to the front; `None` if the object is not in the collection. |
