# OSC Library

```python
from osc import *
```

The OSC (Open Sound Control) library supports communication with OSC-enabled devices (e.g., smartphones, tablets, other computers, etc.).

OSC devices communicate via the Internet, so they do not have to be connected via cable. They could be anywhere – in the same room, in different buildings, or across the globe.

| Contents | Description |
|---|---|
| [OscIn](oscin/index.md) | Receive OSC messages from another device. |
| [OscOut](oscout/index.md) | Send OSC messages to another device. |
| [OscMessage](oscmessage/index.md) | Hold an OSC message's address and arguments. |

## OSC Messages

OSC messages consist of an *address* and optional *arguments*, e.g., “/oscillator/4/frequency 440.0”:

- *Address* patterns look like a URL, e.g., “/oscillator/4/frequency”, “/button/1”, “slider/3”, etc. Any address is possible, as long as both OSC input and output devices use the same values. You can create your own, or use what a particular OSC device sends, e.g., [TouchOSC](https://hexler.net/software/touchosc).

- *Arguments* may be integers, floats, strings, and booleans. OSC messages may include an arbitrary number of arguments (zero or more).

## Receiving and Sending OSC Messages

The OSC library provides two types of objects, [OscIn](oscin/index.md) objects and [OscOut](oscout/index.md) objects:

- [OscIn](oscin/index.md) objects receive incoming OSC messages from OSC devices (e.g., an OSC-enabled smartphone, or tablet).

- [OscOut](oscout/index.md) objects send OSC messages to devices (e.g., computers) that listen for incoming OSC events.

You could use a collection of OscIn and OscOut objects to synchronize (or share data between) two different programs on the same computer, or several computers used in an installation.
