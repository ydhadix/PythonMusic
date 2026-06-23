# getBoundingBox()

Return the smallest upright box that surrounds the object.

The box's own corners are never tilted, so the bounding box grows as the object rotates. For the object's actual (possibly tilted) corners instead, use [getEndpoints()](getEndpoints.md).

**NOTE:** This function isn't available to [Displays](../../display/index.md).

## Parameters

Once an object `item` has been created, you can use the following function:

```python
item.getBoundingBox()
```

## Returns

`return xPoints, yPoints`

| Value | Type | Description |
|---|---|---|
| xPoints | `list[int or float]` | The horizontal positions of the box's four corners, in pixels. |
| yPoints | `list[int or float]` | The vertical positions of the box's four corners, in pixels. |
