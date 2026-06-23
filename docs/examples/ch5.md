# Chapter 5: Iteration and Lists

***Topics:***   *Iteration, Python for loop, arpeggiators, constants, list operations, range(), frange(), FX-35 Octoplus, DNA music.*

Most processes in nature and in human culture involve iteration or repetition at different levels of scale.  This chapter introduces Python constructs for iteration. More information is provided in the [reference textbook](https://goo.gl/Y1VM5t).

Here is code from this chapter:

- [Play an arpeggio pattern using absolute pitches](#play-an-arpeggio-pattern-using-absolute-pitches)
- [Play an arpeggio pattern using relative pitches](#play-an-arpeggio-pattern-using-relative-pitches)
- [Build a Scale Tutor](#build-a-scale-tutor)
- [Generate a piano roll interactively](#generate-a-piano-roll-interactively)
- [Reverse the notes in a phrase](#reverse-the-notes-in-a-phrase)
- [Create a music effect based on the DOD FX-35 guitar pedal](#create-a-music-effect-based-on-the-dod-fx-35-guitar-pedal)
- [Create DNA music](#create-dna-music)

---

## Play an arpeggio pattern using absolute pitches

This code sample ([Ch. 5, p. 128](https://goo.gl/Y1VM5t)) **demonstrates how to play an arpeggio pattern using absolute pitches**.  In other words, the arpeggio is fixed in a particular musical key (in this case C major).

```python linenums="1" title="arpeggiator1.py"
--8<-- "examples/_snippets/arpeggiator1.py"
```

It plays this sound (if you type 7 as input):

<audio controls preload="none" src="../../audio/arpeggiator1.wav"></audio>

---

## Play an arpeggio pattern using relative pitches

This code sample ([Ch. 5, p. 131](https://goo.gl/Y1VM5t)) **demonstrates how to play an arpeggio pattern using relative pitches**.  This makes the arpeggiator a little more flexible.  The relative pitches are added to a root note (e.g., C4) provided through user input.

```python linenums="1" title="arpeggiator2.py"
--8<-- "examples/_snippets/arpeggiator2.py"
```

It plays this sound (if you type G3 and 7 as inputs):

<audio controls preload="none" src="../../audio/arpeggiator2.wav"></audio>

---

## Build a Scale Tutor

The following program ([Ch. 5, p. 136](https://goo.gl/Y1VM5t)) demonstrates how to **output the notes (pitches) in a particular scale**.

```python linenums="1" title="scaleTutor.py"
--8<-- "examples/_snippets/scaleTutor.py"
```

---

## Generate a piano roll interactively

This code sample ([Ch. 5, p. 138](https://goo.gl/Y1VM5t)) demonstrates **how to construct an interactive piano roll generator**.  The program allows us to specify which MIDI instrument to use.   As is, it accepts only one melodic line.  It may be extended to accept more lines.

```python linenums="1" title="pianoRollGenerator.py"
--8<-- "examples/_snippets/pianoRollGenerator.py"
```

---

## Reverse the notes in a phrase

This code sample ([Ch. 5, p. 144](https://goo.gl/Y1VM5t)) **demonstrates how to reverse the notes in a phrase**. This is equivalent to the *Mod.retrograde()* function.

```python linenums="1" title="retrograde1.py"
--8<-- "examples/_snippets/retrograde1.py"
```

To implement the functionality of *Mod.retrograde()* precisely, we would be working with an existing phrase. The following **uses the existing phrase’s notes**:

```python linenums="1" title="retrograde2.py"
--8<-- "examples/_snippets/retrograde2.py"
```

Yet another way would be to iterate through the note list in reverse order directly.  The following code demonstrates this:

```python linenums="1" title="retrograde3.py"
--8<-- "examples/_snippets/retrograde3.py"
```

---

## Create a music effect based on the DOD FX-35 guitar pedal

This code sample ([Ch. 5, p. 147](https://goo.gl/Y1VM5t)) **shows how to implement a more advanced version of a classic guitar effect box**, the DOD FX-35 Octoplus. The FX-35 Octoplus generates a note one octave below the original note, allowing guitarists to add “body” to their sound, or play bass lines on regular guitars. Here we generate one octave below plus a fifth below, creating a “power chord” effect from a single melodic line.

```python linenums="1" title="octoplus.py"
--8<-- "examples/_snippets/octoplus.py"
```

When saved, the two MIDI files sound like this (first the original, then the effect):

<audio controls preload="none" src="../../audio/octoplusOriginal.wav"></audio>

<audio controls preload="none" src="../../audio/octoplusEffect.wav"></audio>

---

## Create DNA music

Many researchers have explored ways to **convert human proteins into music**. This conversion (also known as sonification) allows people to better understand and study the structures and interdependencies in genetic material. In one study, Takahashi and Miller made music from the amino acid sequence in a human protein ([Takahashi and Miller, 2007](http://www.ncbi.nlm.nih.gov/pubmed/17477882)).

The code sample below ([Ch. 5, p. 150](https://goo.gl/Y1VM5t)) builds on their technique.

```python linenums="1" title="proteinMusic.py"
--8<-- "examples/_snippets/proteinMusic.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/proteinMusic.wav"></audio>
