# IannixOut

IanniX is a graphic sequencer. Use an IannixOut to build its score (curves, points, triggers, and cursors) and to control playback.

You can make several IannixOut objects to reach several IanniX installations.

## Creating a IannixOut

You can create a IannixOut using the following functions:

```python
iannixout = IannixOut()
```

```python
IannixOut(ipAddress, port)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ipAddress` | `str` | `'127.0.0.1'` | The IP address of the computer running IanniX. Defaults to this computer. |
| `port` | `int` | `57111` | The port IanniX is listening on. |

For example,

```python
iannixout = IannixOut("168.1.0.1", 57800)
```

## Functions

Once a IannixOut `iannixout` has been created, the following functions are available.

| Function | Description |
|---|---|
| [`iannixout.addPointToCurve(curveID)`](addPointToCurve.md) | Add a point to a curve in the IanniX score. |
| [`iannixout.addPointListToCurve(curveID, listPoints)`](addPointListToCurve.md) | Add many points to a curve in the IanniX score at once. |
| [`iannixout.addCurve(curveID, x, y, z)`](addCurve.md) | Add a new curve to the IanniX score. |
| [`iannixout.removeCurve(curveID)`](removeCurve.md) | Remove a curve from the IanniX score. |
| [`iannixout.addTrigger(triggerID, x, y, z)`](addTrigger.md) | Add a trigger to the IanniX score at the given coordinates. |
| [`iannixout.removeTrigger(triggerID)`](removeTrigger.md) | Remove a trigger from the IanniX score. |
| [`iannixout.addCursor(curveID, cursorID)`](addCursor.md) | Add a cursor to a curve in the IanniX score. |
| [`iannixout.removeCursor(cursorID)`](removeCursor.md) | Remove a cursor from the IanniX score. |
| [`iannixout.clear()`](clear.md) | Remove every object from the IanniX score. |
| [`iannixout.play()`](play.md) | Start the IanniX score playing. |
| [`iannixout.stop()`](stop.md) | Stop the IanniX score. |
| [`iannixout.fastRewind()`](fastRewind.md) | Fast-rewind the IanniX score. |
| [`iannixout.sendMessage(oscAddress)`](sendMessage.md) | Send an OSC message to the connected device. |
