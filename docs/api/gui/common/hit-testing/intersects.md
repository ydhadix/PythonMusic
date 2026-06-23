# intersects()

Report whether this object overlaps another.

## Parameters

Once an object `item` has been created, you can use the following function:

```python
item.intersects(other)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `other` | `Drawable` | _required_ | The other GUI object to test against. |

## Returns

`return otherIsIntersecting`

| Value | Type | Description |
|---|---|---|
| otherIsIntersecting | `bool` | `True` if the two objects overlap, `False` otherwise. |
