# Chapter 3: Organization and Data

***Topics:*** *Notes, phrases, parts, scores, Python lists, Ludwig van Beethoven, scales, MIDI instruments, Harold Faltermeyer, chords, Bruce Hornsby, 2Pac, Joseph Kosma, drums and other percussion, drum machines, Deep Purple, top-down design, reading and writing MIDI files.*

In this chapter, we introduce Python data structures for music making.  We look at some of the Python music data objects and how they represent musical information.  You should already know [how to create notes and rests, and write basic Python programs that play a note, or that output a value, from chapter 2](ch2.md).

More information is provided in the [reference textbook](https://goo.gl/Y1VM5t).

Here is code from this chapter:

- [Play a simple musical theme](#play-a-simple-musical-theme)
- [Play a musical theme setting the instrument and tempo](#play-a-musical-theme-setting-the-instrument-and-tempo)
- [Play a chord progression](#play-a-chord-progression)
- [Create music with various melodic lines sounding simultaneously](#create-music-with-various-melodic-lines-sounding-simultaneously)
- [A Jazz trio arrangement of “Autumn Leaves”](#a-jazz-trio-arrangement-of-autumn-leaves)
- [Play a drum sound](#play-a-drum-sound)
- [Create a drum machine pattern](#create-a-drum-machine-pattern)
- [Play opening theme of “Smoke on the Water”](#play-opening-theme-of-smoke-on-the-water)

---

## Play a simple musical theme

This code sample ([Ch. 3, p. 56](http://goo.gl/Io4kLk)) demonstrates how to use a [phrase](../api/music/transcription/phrase/index.md) to **create a melody**.  It generates the theme from one of the most popular classical pieces, Ludwig van Beethoven’s Bagatelle No. 25 in A minor for solo piano, commonly known as “Für Elise” (for Elise).

```python linenums="1" title="furElise.py"
--8<-- "examples/_snippets/furElise.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/furElise.wav"></audio>

---

## Play a musical theme setting the instrument and tempo

This code sample ([Ch. 3, p. 63](http://goo.gl/Io4kLk)) demonstrates how to **set the instrument and tempo of a phrase**.  It creates  Harold Faltermeyer’s electronic instrumental theme from the 1984 film Beverly Hills Cop.

```python linenums="1" title="axelF.py"
--8<-- "examples/_snippets/axelF.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/axelF.wav"></audio>

Here is the complete list of [MIDI instruments](../api/music/constants/instrument.md).  You can modify the above program to get different sounds.

**Advice on Setting Instrument and Tempo**

Follow this for best results:

- If your program creates **only a single Phrase, you should set the instrument and tempo at the Phrase level** (see above).
- If your program has **several Phrases, you should set the instrument at the Part level, and set the tempo at the Part or Score level**. (see [further below](#create-music-with-various-melodic-lines-sounding-simultaneously)).

Setting the instrument and tempo at the highest musical subdivision **ensures the MIDI synthesizer will play things correctly**.  If not, you may get some surprising results, as phrases with different instruments and tempos may be played via the same MIDI channel producing musically garbled output.

---

## Play a chord progression

This code sample ([Ch. 3, p. 67](http://goo.gl/Io4kLk)) demonstrates how to **create chords.  **It plays the main chord progression from Bruce Hornsby’s “The Way It Is” (1986).

```python linenums="1" title="theWayItIs.py"
--8<-- "examples/_snippets/theWayItIs.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/theWayItIs.wav"></audio>

The next code sample ([Ch. 3, p. 68](http://goo.gl/Io4kLk)) demonstrates a **more efficient way to create chords** via Python lists.  It generates the main chord progression from 2Pac’s (Tupac Shakur’s) “Changes” (1998).  It so happens that this is the same chord progression as in Bruce Hornsby’s “The Way It Is”, above.

```python linenums="1" title="changesByTupac.py"
--8<-- "examples/_snippets/changesByTupac.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/changesByTupac.wav"></audio>

---

## Create music with various melodic lines sounding simultaneously

This code sample ([Ch. 3, p. 72](http://goo.gl/Io4kLk)) demonstrates how to **create musical parts that contain different melodies**.  It plays an excerpt from Haydn’s “String Quartet”, Opus 64 no 5, which consists of four overlapping phrases, using a MIDI strings sound.

```python linenums="1" title="stringQuartet.py"
--8<-- "examples/_snippets/stringQuartet.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/stringQuartet.wav"></audio>

---

## A Jazz trio arrangement of “Autumn Leaves”

This code sample ([Ch. 3, p. 77](http://goo.gl/Io4kLk)) demonstrates how to **create a score containing different parts, each containing a different phrase**.  This is a complete example of the *Score*, *Part*, *Phrase*, *Note* data structure.  It generates the theme from “Autumn Leaves”.

```python linenums="1" title="autumnLeaves.py"
--8<-- "examples/_snippets/autumnLeaves.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/autumnLeaves.wav"></audio>

---

## Play a drum sound

The MIDI standard allows us to write percussive (e.g., drum) parts.  MIDI has 16 channels (numbered 0 to 15).  Of these, **channel 9 is reserved for percussion**.

When adding notes to a *Part* object assigned to channel 9, the pitch of the note determines which percussive instrument to play.  So, whereas for other channels (0-8 and 10-15) the MIDI pitch corresponds to the note’s frequency (or piano key number), for channel 9 the MIDI pitch corresponds to a particular percussive sound (without relationship to pitch).  The General MIDI standard suggests a [mapping between MIDI pitch values and percussion sounds](../api/music/constants/percussion.md).

This code sample ([Ch. 3, p. 80](http://goo.gl/Io4kLk)) demonstrates how to **play a single drum sound**.

```python linenums="1" title="drumExample.py"
--8<-- "examples/_snippets/drumExample.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/drumExample.wav"></audio>

---

## Create a drum machine pattern

Given its power as a musical instrument, a drum machine may form an integral part of a composition or performance, in that it can play complex rhythmic patterns that could not possibly be performed by a single human drummer, or could be hard to perform (without errors) even by a group of drummers.  Drum machines can easily be programmed to generate rhythmic patterns, from the simple to the intricate, using a wide variety of percussive sounds. Let’s see how.

This code sample ([Ch. 3, p. 81](http://goo.gl/Io4kLk)) **implements a drum machine pattern** consisting of bass (kick), snare, and hi-hat sounds.  It uses many notes, three phrases, a part and a score, with each layer adding additional rhythms.

```python linenums="1" title="drumMachinePattern1.py"
--8<-- "examples/_snippets/drumMachinePattern1.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/drumMachinePattern1.wav"></audio>

---

## Play opening theme of “Smoke on the Water”

Now that we know how to create drum parts, we can write programs that create more complete music from various genres.

This code sample ([Ch. 3, p. 83](http://goo.gl/Io4kLk)) demonstrates how to **combine drums with other instruments** by creating the opening of Deep Purple’s “Smoke on the Water,” a rock riff from 1972. It combines melody, chords (actually, power-chords constructed from two simultaneous pitches), and drums.

The emphasis here is on demonstrating how to combine the various building elements we have seen so far.

```python linenums="1" title="DeepPurple.SmokeOnTheWater.py"
--8<-- "examples/_snippets/DeepPurple.SmokeOnTheWater.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/DeepPurple.SmokeOnTheWater.wav"></audio>
