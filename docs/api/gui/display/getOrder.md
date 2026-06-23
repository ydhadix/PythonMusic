# getOrder()

Return the layer a GUI object sits on.

```python
display.getOrder(item)
```

## Parameters

```python
display.getOrder(item)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item` | `Drawable` | _required_ | The GUI object to look up. |

## Returns

`return order`

| Value | Type | Description |
|---|---|---|
| order | `int` | The object's layer, where 0 is closest to the front; None if the object is not on the display. |
