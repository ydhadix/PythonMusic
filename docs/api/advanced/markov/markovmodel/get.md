# get()

Pick a random symbol to follow a context, weighted by how often each was seen.

```python
markovmodel.get(tupleOfSymbols)
```

The context must already exist in the model.

## Parameters

```python
markovmodel.get(tupleOfSymbols)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tupleOfSymbols` | `tuple` | _required_ | The context to follow on from. |

## Returns

```python
symbol
```
