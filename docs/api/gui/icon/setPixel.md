# setPixel()

Set the color of one pixel.

```python
icon.setPixel(column, row, color)
```

The image origin (0, 0) is at the top-left.

## Parameters

```python
icon.setPixel(column, row, color)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `column` | `int` | _required_ | The pixel's column (its horizontal position in the image). |
| `row` | `int` | _required_ | The pixel's row (its vertical position in the image). |
| `color` | `list[int]` | _required_ | The new red, green, and blue values, for example [255, 0, 0]. |
