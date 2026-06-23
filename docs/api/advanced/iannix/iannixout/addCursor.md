# addCursor()

Add a cursor to a curve in the IanniX score.

```python
iannixout.addCursor(curveID, cursorID)
```

A cursor travels along its curve as the score plays.

## Parameters

```python
iannixout.addCursor(curveID, cursorID, offset=0.0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `curveID` | `int or str` | _required_ | The ID of the curve to place the cursor on. |
| `cursorID` | `int or str` | _required_ | The ID to give the new cursor. |
| `offset` | `float` | `0.0` | How far along the curve to start the cursor, in seconds from the start of the curve. |
