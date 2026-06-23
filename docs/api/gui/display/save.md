# save()

Save a picture of the display to JPG or PNG image file.

## Parameters

Once an object `display` has been created, you can use the following functions:

```python
display.save(filename)
```

```python
display.save(filename, width, height)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` | _required_ | The file to write, ending in ".jpg" or ".png". |
| `width` | `int or float` | `None` | The width of the saved image, in pixels. Defaults to the display's width. |
| `height` | `int or float` | `None` | The height of the saved image, in pixels. Defaults to the display's height. |
