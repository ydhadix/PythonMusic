# getBoundingBox()

Return the smallest upright box that surrounds the object.

```python
hfader.getBoundingBox()
```

The box's own corners are never tilted, so it grows as the object rotates. For the object's actual (possibly tilted) corners instead, use [getEndpoints()](getEndpoints.md).

## Returns

`return xPoints, yPoints`

| Value | Type | Description |
|---|---|---|
| xPoints | `list[int or float]` | The horizontal positions of the box's four corners, in pixels. |
| yPoints | `list[int or float]` | The vertical positions of the box's four corners, in pixels. |
