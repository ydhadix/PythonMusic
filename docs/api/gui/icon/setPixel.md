# setPixel()

Set the color of one pixel.  The image origin (0, 0) is at the top-left.

## Parameters

Once an object `icon` has been created, you can use the following function:

```python
icon.setPixel(column, row, color)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `column` | `int` | _required_ | The pixel's column (its horizontal position in the image). |
| `row` | `int` | _required_ | The pixel's row (its vertical position in the image). |
| `color` | `list[int]` | _required_ | The new red, green, and blue values, for example [255, 0, 0].<br>You may add a fourth alpha value, for example [255, 0, 0, 255].  If omitted, the pixel is fully opaque. |
