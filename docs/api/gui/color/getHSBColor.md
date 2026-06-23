# getHSBColor()

Create a Color from HSB (hue, saturation, brightness) values.

```python
Color.getHSBColor(hue, saturation, brightness)
```

Color.getHSBColor is a static utility. Call it on the class itself, for example Color.getHSBColor().

## Parameters

```python
Color.getHSBColor(hue, saturation, brightness)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `hue` | `float` | _required_ | The hue, from 0.0 to 1.0. |
| `saturation` | `float` | _required_ | The saturation, from 0.0 to 1.0. |
| `brightness` | `float` | _required_ | The brightness, from 0.0 to 1.0. |

## Returns

`return hsbColor`

| Value | Type | Description |
|---|---|---|
| hsbColor | `Color` | The matching color. |
