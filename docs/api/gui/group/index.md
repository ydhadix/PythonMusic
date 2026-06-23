# Group

Bundle several GUI objects (including other groups!) so they move, turn, and scale together.

## Creating a Group

You can create a Group using the following functions:

```python
Group()
```

```python
Group(itemList)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `itemList` | `list[Drawable]` | `[]` | The objects to start the group with. |

For example,

```python
group = Group(itemList)
```

where `itemList` is a list of GUI objects.  Moving, resizing, and rotating the group also changes the items within it accordingly.

Once created, you can add it to a [Display](../display/index.md) using the Display's [add()](../common/collection/add.md) function.

## Functions

Once a Group has been created, the following functions are available:

- [Collection](../common/index.md#collection-functions)
- [Position](../common/index.md#position-functions)
- [Size](../common/index.md#size-functions)
- [Rotation](../common/index.md#rotation-functions)
- [Visibility](../common/index.md#visibility-functions)
- [Information](../common/index.md#information-functions)
- [Hit Testing](../common/index.md#hit-testing-functions)
- [Events](../common/index.md#event-functions)
