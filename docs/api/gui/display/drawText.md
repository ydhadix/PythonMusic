# drawText()

Draw a line of text straight onto the display.

```python
display.drawText(text, x, y)
```

Same as [drawLabel()](drawLabel.md).

## Parameters

```python
display.drawText(text, x, y, color=Color.BLACK, font=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | _required_ | The text to draw. |
| `x` | `int or float` | _required_ | The horizontal position of the top-left corner, in pixels. |
| `y` | `int or float` | _required_ | The vertical position of the top-left corner, in pixels. |
| `color` | `Color` | `Color.BLACK` | The text color. |
| `font` | `Font` | `None` | The font, for example Font("Serif", Font.ITALIC, 16). If omitted, the default font is used. |
