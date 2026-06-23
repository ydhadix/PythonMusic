# onClose()

Set up a function to call right before the display closes.

```python
display.onClose(action)
```

Called whether the display is closed with the mouse, the keyboard, or [close()](close.md). Use it to clean up, play a sound, update other displays, and so on.

## Parameters

```python
display.onClose(action)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `action` | `function` | _required_ | The function to call; it receives no parameters. |
