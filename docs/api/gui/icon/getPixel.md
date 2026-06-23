# getPixel()

Return the color of one pixel.

```python
icon.getPixel(column, row)
```

The image origin (0, 0) is at the top-left.

## Parameters

```python
icon.getPixel(column, row)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `column` | `int` | _required_ | The pixel's column (its horizontal position in the image). |
| `row` | `int` | _required_ | The pixel's row (its vertical position in the image). |

## Returns

`return pixel`

| Value | Type | Description |
|---|---|---|
| pixel | `list[int]` | The pixel's red, green, and blue values, for example [255, 0, 0]. |
