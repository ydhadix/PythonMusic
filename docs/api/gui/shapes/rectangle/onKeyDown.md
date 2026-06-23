# onKeyDown()

Set up a function to call when a key is pressed down.

```python
rectangle.onKeyDown(action)
```

Holding a key down may call the function repeatedly, at the keyboard's repeat rate.

## Parameters

```python
rectangle.onKeyDown(action)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `action` | `function` | _required_ | The function to call; it receives one parameter, the virtual key code as an int, for example VK_SHIFT or VK_A. |
