# selectMidiOutput()

Connect to a preferred output MIDI device, or open a window to pick one.

```python
midiout.selectMidiOutput()
```

If the named device is not available, a window opens listing the output devices found.

## Parameters

```python
midiout.selectMidiOutput(preferredDevice='')
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `preferredDevice` | `str` | `''` | The name of the output device to connect to. If omitted or unavailable, a selection window opens. |
