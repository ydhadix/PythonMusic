# getEndpoints()

Return the object's four corners.

```python
dropdownlist.getEndpoints()
```

The corners turn with the object, so a rotated object's endpoints are its actual tilted corners. For the upright box around the object instead, use [getBoundingBox()](getBoundingBox.md).

## Returns

`return xPoints, yPoints`

| Value | Type | Description |
|---|---|---|
| xPoints | `list[int or float]` | The horizontal positions of the four corners, in pixels. |
| yPoints | `list[int or float]` | The vertical positions of the four corners, in pixels. |
