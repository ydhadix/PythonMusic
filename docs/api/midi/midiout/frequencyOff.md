# frequencyOff()

Stop a frequency from sounding on the device.

```python
midiout.frequencyOff(frequency)
```

If the frequency is not sounding on this channel, nothing happens.

## Parameters

```python
midiout.frequencyOff(frequency, channel=0)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `frequency` | `float` | _required_ | The frequency to stop, in hertz (8.17 to 12600.0). |
| `channel` | `int` | `0` | The channel it is playing on, from 0 to 15. |
