# learn()

Learn the patterns in a sequence of symbols.

```python
markovmodel.learn(listOfSymbols)
```

Pulls the n-grams out of the list and adds their transitions to the model. Call it more than once to keep training the model on further sequences.

## Parameters

```python
markovmodel.learn(listOfSymbols)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `listOfSymbols` | `list` | _required_ | The sequence to learn from. |
