# Font

Represent a text font with a name, style, and size.

Use a Font to change how text looks on a [Label](../label/index.md), [TextField](../textfield/index.md), or [TextArea](../textarea/index.md).

## Creating a Font

You can create a Font using the following functions:

```python
Font(name)
```

```python
Font(name, style, size)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | _required_ | The font name, for example "Serif", "Dialog", or "TimesRoman". |
| `style` | `tuple` | `PLAIN` | The text style, one of `Font.PLAIN`, `Font.BOLD`, `Font.ITALIC`, or `Font.BOLDITALIC`. |
| `size` | `int` | `-1` | The point size. If left as the default, the standard size is used. |

For example,

```python
font = Font("Arial", Font.ITALIC, 16)
```

Once created, you can use it with the setFont() function from a [Label](../label/index.md), [TextField](../textfield/index.md), or [TextArea](../textarea/index.md) object.

## Functions

Once a Font has been created, the following functions are available:

| Function | Description |
|---|---|
| [`getName()`](getName.md) | Return the font's name. |
| [`setName(name)`](setName.md) | Set the font's name. |
| [`getStyle()`](getStyle.md) | Return the font's style. |
| [`setStyle(style)`](setStyle.md) | Set the font's style. |
| [`getSize()`](getSize.md) | Return the font's point size. |
| [`setSize(size)`](setSize.md) | Set the font's point size. |
