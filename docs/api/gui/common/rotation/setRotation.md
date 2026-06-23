# setRotation()

Turn the object to a given angle.

By default the object turns about its own center. Give an anchor point to turn it about that point instead.

## Parameters

Once an object `item` has been created, you can use the following functions:

```python
item.setRotation(rotation)
```

```python
item.setRotation(rotation, anchorX, anchorY)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `rotation` | `int or float` | _required_ | The angle to turn to, in degrees, counter-clockwise. |
| `anchorX` | `int or float` | `None` | The horizontal position of the point to turn about, in pixels. Defaults to the object's center. |
| `anchorY` | `int or float` | `None` | The vertical position of the point to turn about, in pixels. Defaults to the object's center. |
