# save()

Save a picture of the display to an image file.

```python
display.save(filename)
```

## Parameters

```python
display.save(filename, width=None, height=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` | _required_ | The file to write, ending in ".jpg" or ".png". |
| `width` | `int or float` | `None` | The width of the saved image, in pixels. Defaults to the display's width. |
| `height` | `int or float` | `None` | The height of the saved image, in pixels. Defaults to the display's height. |
