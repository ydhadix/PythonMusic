# encloses()

Report whether this object completely contains another.

## Parameters

Once an object `item` has been created, you can use the following function:

```python
item.encloses(other)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `other` | `Drawable` | _required_ | The other object to test against. |

## Returns

`return otherIsInside`

| Value | Type | Description |
|---|---|---|
| otherIsInside | `bool` | `True` if the other object lies entirely inside this one, `False` otherwise. |
