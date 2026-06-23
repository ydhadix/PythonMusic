# addItem()

Add an item to the menu.

## Parameters

Once an object `menu` has been created, you can use the following functions:

```python
menu.addItem()
```

```python
menu.addItem(item)
```

```python
menu.addItem(item, action)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item` | `str` | `''` | The item's text, as shown in the menu. |
| `action` | `function` | `None` | The function to call when the item is selected; it receives no parameters. |
