# isConnected()

Report whether the model can continue from a context.

```python
compositemarkovmodel.isConnected(context)
```

The model is connected at a context when that context has at least one known transition at some order, so generation could carry on from it.

## Parameters

```python
compositemarkovmodel.isConnected(context)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `context` | `tuple` | _required_ | The context to check. |

## Returns

`return connected`

| Value | Type | Description |
|---|---|---|
| connected | `bool` | True if the model has a transition for the context, False otherwise. |
