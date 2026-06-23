# put()

Add a single transition to the model by hand.

```python
markovmodel.put(tupleOfSymbols)
```

Records that symbol can follow tupleOfSymbols. [learn()](learn.md) builds these for you, so use put() only to add transitions directly.

## Parameters

```python
markovmodel.put(tupleOfSymbols, symbol=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tupleOfSymbols` | `tuple` | _required_ | The context (the run of symbols leading up to the next one). |
| `symbol` | `optional` | `None` | The symbol that follows the context. None marks the end of a sequence. |
