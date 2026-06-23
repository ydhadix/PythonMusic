# getEndpoints()

Return the polyline's corners.

```python
polyline.getEndpoints()
```

The corners turn with the shape, so a rotated polyline's endpoints are its actual tilted corners.

## Returns

`return xPoints, yPoints`

| Value | Type | Description |
|---|---|---|
| xPoints | `list[int or float]` | The horizontal positions of the corners, in pixels. |
| yPoints | `list[int or float]` | The vertical positions of the corners, in pixels. |
