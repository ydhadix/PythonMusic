# getPixel()

Return the color of one pixel.  The icon origin (0, 0) is at the top-left.

## Parameters

Once an object `icon` has been created, you can use the following function:

```python
icon.getPixel(column, row)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `column` | `int` | _required_ | The pixel's column (its horizontal position in the icon). |
| `row` | `int` | _required_ | The pixel's row (its vertical position in the icon). |

## Returns

`return pixel`

| Value | Type | Description |
|---|---|---|
| pixel | `list[int]` | The pixel's red, green, blue, and alpha values, for example [255, 0, 0, 255]. |
