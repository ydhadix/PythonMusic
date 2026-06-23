# crop()

Crop the image to a rectangular region.

```python
icon.crop(x, y, width, height)
```

Keeps the part of the image starting at (x, y) and extending the given width and height; the rest is discarded.

## Parameters

```python
icon.crop(x, y, width, height)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x` | `int or float` | _required_ | The horizontal start of the region, in pixels from the image's top-left. |
| `y` | `int or float` | _required_ | The vertical start of the region, in pixels from the image's top-left. |
| `width` | `int or float` | _required_ | The width of the region to keep, in pixels. |
| `height` | `int or float` | _required_ | The height of the region to keep, in pixels. |
