# setPixels()

Replace every pixel in the image.

The pixels are arranged as a list of rows, each row a list of pixels, each pixel a list of red, green, blue, and (optional) alpha values. The image's top-left pixel is at [0][0].

## Parameters

Once an object `icon` has been created, you can use the following function:

```python
icon.setPixels(pixels)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pixels` | `list[list[list[int]]]` | _required_ | The new pixels, by row then column, each as [red, green, blue].<br>You may add a fourth alpha value as [red, green, blue, alpha].  If omitted, the pixel is fully opaque. |
