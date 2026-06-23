# get()

Pick a random symbol to follow a context, using the longest order that fits.

```python
compositemarkovmodel.get(tupleOfSymbols)
```

Tries the highest order first and falls back to shorter contexts as needed.

## Parameters

```python
compositemarkovmodel.get(tupleOfSymbols)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tupleOfSymbols` | `tuple` | _required_ | The context to follow on from. |

## Returns

```python
nextSymbol
```
