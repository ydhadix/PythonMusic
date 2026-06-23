# addItemList()

Add several items to the menu at once.

The two lists are parallel and must be the same length: each item's text is paired with the function to call when it is selected.

## Parameters

Once an object `menu` has been created, you can use the following functions:

```python
menu.addItemList()
```

```python
menu.addItemList(itemList)
```

```python
menu.addItemList(itemList, actionList)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `itemList` | `list[str]` | `['']` | The items' text. |
| `actionList` | `list[function]` | `[]` | The functions to call, one per item. |
