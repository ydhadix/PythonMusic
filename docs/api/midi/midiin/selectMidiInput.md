# selectMidiInput()

Connect to a preferred input MIDI device, or open a window to pick one.

```python
midiin.selectMidiInput()
```

If the named device is not available, a window opens listing the input devices found.

## Parameters

```python
midiin.selectMidiInput(preferredDevice='')
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `preferredDevice` | `str` | `''` | The name of the input device to connect to. If omitted or unavailable, a selection window opens. |
