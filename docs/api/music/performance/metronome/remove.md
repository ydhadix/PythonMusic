# remove()

Remove a scheduled function from the metronome.

```python
metronome.remove(action)
```

If the function was scheduled several times, the earliest one is removed; call again to remove more.

## Parameters

```python
metronome.remove(action)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `action` | `function` | _required_ | The function to remove. |
