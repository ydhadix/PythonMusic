# setPixels()

Replace every pixel in the image.

```python
icon.setPixels(pixels)
```

The pixels are arranged as a list of rows, each row a list of pixels, each pixel a list of red, green, and blue values. The image's top-left pixel is at [0][0].

## Parameters

```python
icon.setPixels(pixels)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pixels` | `list[list[list[int]]]` | _required_ | The new pixels, by row then column, each as [red, green, blue]. |
