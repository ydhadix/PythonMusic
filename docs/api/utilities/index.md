# Mapping Values

Each PythonMusic library includes helpful functions for mapping values from one range (say, 5 to 10), to another range (say, -35 to 120).

| Function | Description |
|---|---|
| [`mapValue(value, minValue, maxValue, minResult, maxResult)`](mapValue.md) |  Takes a number within one range and returns its equivalent within another range. |
| [`map(value, minValue, maxValue, minResult, maxResult)`](map.md) | Same as mapValue, except values can be placed outside of the first range to project its equivalent outside of another range. |
| [`mapScale(value, minValue, maxValue, minResult, maxResult)`](mapScale.md) |  Same as mapValue(), except results are rounded to the nearest pitch in a given MIDI scale. |
| [`mapValueList(valueList, minValue, maxValue, minResult, maxResult)`](mapValueList.md) | Convert a list of numbers from one range to their matching places in another range. |
| [`mapList(valueList, minValue, maxValue, minResult, maxResult)`](mapList.md) | Convert a list of numbers from one range to their matching places relative to another range. |
| [`mapScaleList(valueList, minValue, maxValue, minResult, maxResult)`](mapScaleList.md) |  Convert a list of numbers from one range to their matching places in another range, rounded to the nearest MIDI pitch. |
| [`frange(start, stop, step)`](frange.md) | Build a list of evenly spaced numbers, allowing fractional steps. |
| [`xfrange(start, stop, step)`](xfrange.md) | Step through evenly spaced numbers one at a time, allowing fractional steps. |

Map functions are used to expand, contract, or offset data values. They convert a numeric value from one range to another.

For example, mapping the value 0 from the range 0..100 to the range 10..20 results in 10:

```python
>>> mapValue(0, 0, 100, 10, 20)
10
```

Notice how 0 is the leftmost value in its range, as is 10.

Similarly, mapping 50 from the range 0..100 to the range 10..20 results in 15:

```python
>>> mapValue(50, 0, 100, 10, 20)
15
```

Again, notice how 50 is in the middle of its range, and so is 15.

So, map functions maintain the relative position of a value.

**NOTE:** If you use float numbers, mapValue() will return a float value that is properly scaled (preserving accuracy):

```python
>>> mapValue(49 , 0, 100, 10, 20)
14
>>> mapValue(49 , 0, 100, 10.0, 20.0)
14.9
```

Notice how in the second example, 49 was mapped to 14.9, since the destination range was float.
