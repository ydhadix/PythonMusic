# sendMessage()

Send an OSC message to the connected device.

```python
iannixout.sendMessage(oscAddress)
```

A message is an address plus any number of arguments.

## Parameters

```python
iannixout.sendMessage(oscAddress, *args)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `oscAddress` | `str` | _required_ | The OSC address to send to, for example "/first/second/third". *args: Zero or more values to send with the message (numbers, text, or True/False). |
| `*args` |  |  |  |
