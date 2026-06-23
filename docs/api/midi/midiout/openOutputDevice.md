# openOutputDevice()

Open a named output MIDI device.

```python
midiout.openOutputDevice(selectedItem)
```

This is the callback used by the device-selection window; you do not normally call it yourself.

## Parameters

```python
midiout.openOutputDevice(selectedItem)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `selectedItem` | `str` | _required_ | The name of the output device to open. |
