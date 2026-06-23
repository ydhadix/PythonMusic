# getPixels()

Return every pixel in the image.

```python
icon.getPixels()
```

The pixels are arranged as a list of rows, each row a list of pixels, each pixel a list of red, green, and blue values. The image's top-left pixel is at [0][0].

## Returns

`return pixelList`

| Value | Type | Description |
|---|---|---|
| pixelList | `list[list[list[int]]]` | The image's pixels, by row then column, each as [red, green, blue]. |
