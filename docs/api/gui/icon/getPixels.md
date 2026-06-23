# getPixels()

Return every pixel in the image.

The pixels are arranged as a list of rows, each row a list of pixels, each pixel a list of red, green, blue, and alpha values. The image's top-left pixel is at [0][0].

## Parameters

Once an object `icon` has been created, you can use the following function:

```python
icon.getPixels()
```

## Returns

`return pixelList`

| Value | Type | Description |
|---|---|---|
| pixelList | `list[list[list[int]]]` | The image's pixels, by row then column, each as [red, green, blue, alpha]. |
