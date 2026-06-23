# Dynamic Constants

Dynamic or volume of notes (also known as MIDI velocity) is represented as in the MIDI specification using integers from 0 (silent) to 127 (loudest). That’s a total of 128 volume settings.

The music library defines the following dynamic constants:

| Constant | Value |
|---|---|
| `FFF` | `120` |
| `FORTISSIMO`, `FF` | `100` |
| `FORTE`, `F` | `85` |
| `MEZZO_FORTE`, `MF` | `70` |
| `MEZZO_PIANO`, `MP` | `60` |
| `P` | `50` |
| `PIANISSIMO`, `PP` | `25` |
| `PPP` | `10` |
| `SILENT` | `0` |