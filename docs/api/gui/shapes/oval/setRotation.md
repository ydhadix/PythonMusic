# setRotation()

Turn the object to a given angle.

```python
oval.setRotation(rotation)
```

By default the object turns about its own center. Give an anchor point to turn it about that point instead.

## Parameters

```python
oval.setRotation(rotation, anchorX=None, anchorY=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `rotation` | `int or float` | _required_ | The angle to turn to, in degrees, counter-clockwise. |
| `anchorX` | `int or float` | `None` | The horizontal position of the point to turn about, in pixels. Defaults to the object's center. |
| `anchorY` | `int or float` | `None` | The vertical position of the point to turn about, in pixels. Defaults to the object's center. |
