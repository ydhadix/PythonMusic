# save()

Save the icon to a JPG or PNG file.

## Parameters

Once an object `icon` has been created, you can use the following functions:

```python
icon.save(filename)
```

```python
icon.save(filename, width, height)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` | _required_ | The file to write, ending in ".jpg" or ".png". |
| `width` | `int or float` | `None` | The width of the saved icon, in pixels. Defaults to the icon's current width. |
| `height` | `int or float` | `None` | The height of the saved icon, in pixels. Defaults to the icon's current height. |
