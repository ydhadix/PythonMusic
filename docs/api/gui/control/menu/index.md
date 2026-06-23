# Menu

Create a menu, for use on a display's menu bar or as a pop-up.

Every [Display](../../display/index.md) has a menu bar at the top, which is intially empty.  Menu items ("File", "Edit", etc.) can be added to it.

Menus can also be added to a display as pop-up menus (i.e., menus that appear when you press the right mouse button).

## Creating a Menu

You can create a Menu using the following function:

```python
Menu(title)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `str` | _required_ | The menu's name, as shown on the menu bar. |

Once a menu is created, it can be populated using the [addItem()](addItem.md) and [addItemList()](addItemList.md) functions.

Once created, you can add it to a [Display](../../display/index.md) using the Display's [addMenu()](../../display/addMenu.md) or [addPopupMen()](../../display/addPopupMenu.md) function.

## Functions

Once a Menu `menu` has been created, the following functions are available:

| Function | Description |
|---|---|
| [`menu.addItem()`](addItem.md) | Add an item to the menu. |
| [`menu.addItemList()`](addItemList.md) | Add several items to the menu at once. |
| [`menu.addSeparator()`](addSeparator.md) | Add a separator line to the menu. |
| [`menu.addSubmenu(menu)`](addSubmenu.md) | Add a submenu to the menu. |
| [`menu.enable()`](enable.md) | Enable the menu, so its items can be selected. |
| [`menu.disable()`](disable.md) | Disable the menu, graying it out so its items cannot be selected. |
