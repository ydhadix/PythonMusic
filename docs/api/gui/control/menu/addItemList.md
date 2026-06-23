# addItemList()

Add several items to the menu at once.

```python
menu.addItemList()
```

The two lists are parallel and must be the same length: each item's text is paired with the function to call when it is selected.

## Parameters

```python
menu.addItemList(itemList=[''], actionList=[])
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `itemList` | `list[str]` | `['']` | The items' text. |
| `actionList` | `list[function]` | `[]` | The functions to call, one per item. |
