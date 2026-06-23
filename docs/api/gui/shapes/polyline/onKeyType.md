# onKeyType()

Set up a function to call when a key is typed (pressed and released).

```python
polyline.onKeyType(action)
```

## Parameters

```python
polyline.onKeyType(action)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `action` | `function` | _required_ | The function to call; it receives one parameter, the key typed as a string, for example "a", "A", "1", or "/". Upper and lower case are distinguished. |
