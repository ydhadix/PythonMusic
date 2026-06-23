# shake()

Randomly vary the notes' volumes for an uneven, human feel, in place.

```python
Mod.shake(material)
```

## Parameters

```python
Mod.shake(material, amount=20)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `material` | `Phrase, Part, or Score` | _required_ | The music to change. |
| `amount` | `int` | `20` | How strong the effect is. Each volume moves by up to this much, from 0 to 127. |
