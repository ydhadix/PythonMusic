# setTimeSignature()

Set the score's time signature.

```python
score.setTimeSignature(numerator, denominator)
```

For example, setTimeSignature(3, 4) sets 3/4 time.

## Parameters

```python
score.setTimeSignature(numerator, denominator)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `numerator` | `int` | _required_ | The number of beats per measure (the top number). |
| `denominator` | `int` | _required_ | The note value that counts as one beat (the bottom number). |
