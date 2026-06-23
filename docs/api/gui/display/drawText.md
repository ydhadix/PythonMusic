# drawText()

Draw a line of text straight onto the display.

Same as [drawLabel()](drawLabel.md).

## Parameters

Once an object `display` has been created, you can use the following functions:

```python
display.drawText(text, x, y)
```

```python
display.drawText(text, x, y, color, font, visibility)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | _required_ | The text to draw. |
| `x` | `int or float` | _required_ | The horizontal position of the top-left corner, in pixels. |
| `y` | `int or float` | _required_ | The vertical position of the top-left corner, in pixels. |
| `color` | `Color` | `Color.BLACK` | The text color. |
| `font` | `Font` | `None` | The font, for example `Font("Serif", Font.ITALIC, 16)`. If omitted, the default font is used. |
| `visibility` | `int` | `100` | How visible the rectangle is, from 0 (invisible) to 100 (fully visible). |