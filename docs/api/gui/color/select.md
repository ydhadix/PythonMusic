# select()

Open a color-selection dialog and return the color the user picks.

```python
Color.select()
```

Color.select is a static utility. Call it on the class itself, for example Color.select().

## Parameters

```python
Color.select(red=255, green=255, blue=255)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `red` | `int` | `255` | The red component the dialog starts on, from 0 to 255. |
| `green` | `int` | `255` | The green component the dialog starts on, from 0 to 255. |
| `blue` | `int` | `255` | The blue component the dialog starts on, from 0 to 255. |

## Returns

`return red, green, blue`

| Value | Type | Description |
|---|---|---|
| red | `int` | The chosen red component, from 0 to 255. |
| green | `int` | The chosen green component, from 0 to 255. |
| blue | `int` | The chosen blue component, from 0 to 255. |
