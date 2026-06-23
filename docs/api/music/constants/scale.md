# Scale Constants

Scales in the music library are defined as pitch class sets (i.e., chromatic scale degrees within one octave). Scale values range between 0 and 11. The first pitch is often 0, denoting the starting (root) note.

Here are some predefined scales:

| Constant | Value |
|---|---|
| `AEOLIAN_SCALE` | `[0, 2, 3, 5, 7, 8, 10]` |
| `BLUES_SCALE` | `[0, 2, 3, 4, 5, 7, 9, 10, 11]` |
| `CHROMATIC_SCALE` | `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]` |
| `DIATONIC_MINOR_SCALE` | `[0, 2, 3, 5, 7, 8, 10]` |
| `DORIAN_SCALE` | `[0, 2, 3, 5, 7, 9, 10]` |
| `HARMONIC_MINOR_SCALE` | `[0, 2, 3, 5, 7, 8, 11]` |
| `LYDIAN_SCALE` | `[0, 2, 4, 6, 7, 9, 11]` |
| `MAJOR_SCALE` | `[0, 2, 4, 5, 7, 9, 11]` |
| `MELODIC_MINOR_SCALE` | `[0, 2, 3, 5, 7, 8, 9, 10, 11]` |
| `MINOR_SCALE` | `[0, 2, 3, 5, 7, 8, 10]` |
| `MIXOLYDIAN_SCALE` | `[0, 2, 4, 5, 7, 9, 10]` |
| `NATURAL_MINOR_SCALE` | `[0, 2, 3, 5, 7, 8, 10]` |
| `PENTATONIC_SCALE` | `[0, 2, 4, 7, 9]` |

You can define your own scales in a similar way. For instance,

```python
MY_SCALE = [0, 1, 4, 7, 11]
```

Again, scale values may range between 0 and 11.

It is also possible to define microtonal scales.  This is a more advanced topic (see [microtonal music](../microtonality.md)).