# Chapter 4: Transformation and Process

***Topics:***   *Musical patterns and meaning, minimalism, Steve Reich, Mod functions, musical canon, J.S. Bach, Arvo Pärt, viewing musical material, software development process, computer-aided music composition.*

Being able to write down and represent music is an important skill that we have examined in some detail in the previous chapters. In this chapter we focus on another important skill, transforming music to create variations and developing it into longer and more interesting compositions.  More broadly this chapter explores foundational programming skills required to manipulate data.  More information is provided in the [reference textbook](https://goo.gl/Y1VM5t).

Here is code from this chapter:

- [Create Steve Reich’s piece](#create-steve-reichs-piece-piano-phase-1967)
- [Create a simple musical canon, “Row Your Boat”](#create-a-simple-musical-canon-row-your-boat)
- [Create J.S. Bach’s Canon No. 1 on the Goldberg Ground (BWV 1087)](#create-js-bachs-canon-no-1-on-the-goldberg-ground-bwv-1087)
- [Create J.S. Bach’s “Trias Harmonica” canon (BWV 1072)](#create-js-bachs-trias-harmonica-canon-bwv-1072)
- [Create Arvo Part’s “Cantus in Memoriam Benjamin Britten” (1977)](#create-arvo-parts-cantus-in-memoriam-benjamin-britten-1977)
- [Create variations automatically from a theme](#create-variations-automatically-from-a-theme)

---

## Create Steve Reich’s piece, “Piano Phase” (1967)

This code sample ([Ch. 4, p. 94](https://goo.gl/Y1VM5t)) **creates** **Steve Reich’s “Piano Phase”**, a minimalist piece for two pianos involving tempo differences and repetition. The speed difference is quite small, 0.5 beats-per-minute (quarter-notes per minute), so the phase shift is quite gradual, but nevertheless the result is dramatic.

```python linenums="1" title="pianoPhase.py"
--8<-- "examples/_snippets/pianoPhase.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/pianoPhase.wav"></audio>

**A Variation**
Here is [a variation](../articles/steve-reichs-piano-phase.md) of this piece utilizing more [Mod functions](../api/music/composition/mod/index.md) and adding a bass voice.

It plays this sound:

<audio controls preload="none" src="../../audio/pianoPhaseWithBass.wav"></audio>

---

## Create a simple musical canon, “Row Your Boat”

This code sample ([Ch. 4, p. 99](https://goo.gl/Y1VM5t)) demonstrates how to **create a musical canon**.

```python linenums="1" title="rowYourBoat.py"
--8<-- "examples/_snippets/rowYourBoat.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/rowYourBoat.wav"></audio>

---

## Create J.S. Bach’s Canon No. 1 on the Goldberg Ground (BWV 1087)

In 1741, Johann Sebastian Bach (1685 – 1750) wrote the Goldberg Variations (BWV 988) for harpsichord. In 1974 an unknown manuscript was discovered, written in Bach’s hand, containing 14 canons on the first eight notes of the Goldberg aria.

The following program ([Ch. 4, p. 106](https://goo.gl/Y1VM5t)) demonstrates how to use [Mod functions](../api/music/composition/mod/index.md) to **create the first of these 14 canons**. It is built from a theme consisting of eight notes and reversed version (retrograde) played simultaneously.

```python linenums="1" title="JS_Bach.Canon_1.GoldbergGround.BWV1087.py"
--8<-- "examples/_snippets/JS_Bach.Canon_1.GoldbergGround.BWV1087.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/JS_Bach.Canon_1.GoldbergGround.BWV1087.wav"></audio>

---

## Create J.S. Bach’s “Trias Harmonica” canon (BWV 1072)

This code sample ([Ch. 4, p. 108](https://goo.gl/Y1VM5t)) **creates the Trias Harmonica canon (BWV 1072)**. The Trias Harmonica consists of two parts with four separate voices each – a total of 8 overlaid phrases.

```python linenums="1" title="JS_Bach.Canon.TriasHarmonica.BWV1072.py"
--8<-- "examples/_snippets/JS_Bach.Canon.TriasHarmonica.BWV1072.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/JS_Bach.Canon.TriasHarmonica.BWV1072.wav"></audio>

---

## Create Arvo Part’s “Cantus in Memoriam Benjamin Britten” (1977)

This code sample ([Ch. 4, p. 110](https://goo.gl/Y1VM5t)) **creates Arvo Pärt’s “Cantus in Memoriam Benjamin Britten”**.  It creates a single voice descending in stepwise motion the A natural minor scale. This voice is repeated at half tempo several times, creating beautiful harmonic combinations stemming from all permutations of aeolian-scale notes. This is a slightly simplified version of the original piece.

```python linenums="1" title="ArvoPart.CantusInMemoriam.py"
--8<-- "examples/_snippets/ArvoPart.CantusInMemoriam.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/ArvoPart.CantusInMemoriam.wav"></audio>

---

## Create variations automatically from a theme

The following program ([Ch. 4, p. 121](https://goo.gl/Y1VM5t)) demonstrates how to use various [Mod functions](../api/music/composition/mod/index.md) to create novel music from existing material.  For simplicity, this aims for a piece with reasonable (but not perfect) musicality – a piece that can be used to explore musical possibilities, and get new ideas.  Since randomness is involved, every time this program runs will create new variations (some better than others).

```python linenums="1" title="themeAndVariations.py"
--8<-- "examples/_snippets/themeAndVariations.py"
```

It plays this sound:

<audio controls preload="none" src="../../audio/themeAndVariations.wav"></audio>
