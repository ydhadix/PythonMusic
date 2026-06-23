# Chapter 6: Randomness and Choices

***Topics:***   *Randomness and creativity, Mozart, indeterminism, serialism, Python random functions, stochastic music, Iannis Xenakis, probabilities, wind chimes, melody generator, selection, Python if statement, flipping a coin, Russian roulette, throwing dice, realistic drums, relational and logical operators, generative music.*

Computers offer us a source of untamed possibilities in the form of a random number generator. This chapter focuses on ways to tame this source of possibilities to serve our aesthetic purposes.  More information is provided in the [reference textbook](https://goo.gl/Y1VM5t).

Here is code from this chapter:

- [Creating Mozart’s “Musikalisches Würfelspiel”](#creating-mozarts-musikalisches-wurfelspiel)
- [Creating Pierre Cage’s “Structures pour deux Chances”](#creating-pierre-cages-structures-pour-deux-chances)
- [Creating Iannis Xenakis’ stochastic piece,“Concret PH”](#creating-iannis-xenakis-stochastic-piececoncret-ph)
- [Harnessing (or sieving) randomness – wind chimes](#harnessing-or-sieving-randomness-wind-chimes)
- [Music from Brownian motion](#music-from-brownian-motion)
- [Throwing dice](#throwing-dice)
- [Let the drums come alive](#let-the-drums-come-alive)
- [Creating generative music](#creating-generative-music)

---

## Creating Mozart’s “Musikalisches Würfelspiel”

In 1787, Wolfgang Amadeus Mozart wrote “[Musikalisches Würfelspiel](http://en.wikipedia.org/wiki/Musikalisches_W%C3%BCrfelspiel)”, a musical process for generating a 16-measure waltz through randomness – he rolled dice.  In this process, each measure is selected from a set of 11 precomposed chunks of music.

This code sample ([Ch. 6, p. 157](http://goo.gl/Io4kLk)) **demonstrates how to implement a simplified version of Mozart’s musical game**.

```python linenums="1" title="Mozart.MusikalischesWurfelspiel.py"
--8<-- "examples/_snippets/Mozart.MusikalischesWurfelspiel.py"
```

Since randomness is involved, every time it runs, it will generate different outputs.  Here are three examples:

<audio controls preload="none" src="../../audio/Mozart.MusikalischesWurfelspiel1.wav"></audio>

<audio controls preload="none" src="../../audio/Mozart.MusikalischesWurfelspiel2.wav"></audio>

<audio controls preload="none" src="../../audio/Mozart.MusikalischesWurfelspiel3.wav"></audio>

---

## Creating Pierre Cage’s “Structures pour deux Chances”

An interesting way of applying randomness in music is in a style referred to as *chance music*. *Chance music*, also known as *aleatoric music*, is a compositional technique that introduces elements of randomness into the compositional process. John Cage, among other composers, is well known for his aleatoric compositions.  On the other hand, *serialism* involves using deterministic rules to control choices within the compositional process. Pierre Boulez is well known for his serial compositions.

Aleatoric and serial techniques are compositional opposites of each other. Surprisingly, though, the musical outcome can appear to be very similar. This can be observed in these two pieces — the first aleatoric, the second serialist:

- [John Cage, “Music of Changes, Book I”](https://www.youtube.com/watch?v=qOwcpjr9wFA) (1951), and
- [Pierre Boulez, “Structures I for two pianos”](https://www.youtube.com/watch?v=chJJHbkDR9I) (1951-2).

This code sample ([Ch. 6, p. 161](https://goo.gl/Y1VM5t)) capitalizes on this similarity to **create a program where is impossible to determine**, simply by listening to it,** if the compositional approach was aleatoric or a serialist**. This piece is attributed to Pierre Cage.  Pierre Cage is a fictitious composer (a remix of the names, Pierre Boulez and John Cage).

```python linenums="1" title="PierreCage.StructuresPourDeuxChances.py"
--8<-- "examples/_snippets/PierreCage.StructuresPourDeuxChances.py"
```

Since randomness is involved, it will generate output similar (but not identical) to this:

<audio controls preload="none" src="../../audio/PierreCage.StructuresPourDeuxChances.wav"></audio>

---

## Creating Iannis Xenakis’ stochastic piece,“Concret PH”

Stochastic music is a compositional method employed by Iannis Xenakis, as a reaction to the abstractness and complexity of music from the Serialist movement.  Xenakis proposed that the mathematics of probability could be the basis of a more general and manageable compositional technique ([Xenakis 1971](http://books.google.com/books/about/Formalized_music.html?id=I6sQAQAAMAAJ)).

“Concret PH” is a very influential piece of stochastic music. It was created by Xenakis to be played inside the Philips Pavilion in the 1958 World’s Fair in Brussels. This building was designed by architect Le Corbusier, who employed Xenakis as an architect and mathematician at the time.

The following program ([Ch. 6, p. 167](https://goo.gl/Y1VM5t)) **demonstrates how to generate a stochastic piece of music**.  In the original piece, Xenakis used spliced tape of sounds made by burning charcoal. Here, we mimic the sound using the MIDI instrument BREATHNOISE, which at short “bursts” (notes with short duration) sounds much like Xenakis’ original sound elements.

```python linenums="1" title="ConcretPH_Xenakis.py"
--8<-- "examples/_snippets/ConcretPH_Xenakis.py"
```

Since randomness is involved, it will generate output similar (but not identical) to this:

<audio controls preload="none" src="../../audio/ConcretPH_Xenakis.wav"></audio>

---

## Harnessing (or sieving) randomness – wind chimes

As mentioned above, a way to generate artifacts that are aesthetically pleasing, starting with pure randomness, is to filter a random process through a sieve. For example, wind chimes capture random movements of air and force them onto a narrow set of aesthetic possibilities.  The following program ([Ch. 6, p. 169](https://goo.gl/Y1VM5t)) **demonstrates how to create wind chimes out of randomness**.

```python linenums="1" title="windChimes.py"
--8<-- "examples/_snippets/windChimes.py"
```

Since randomness is involved, it will generate output similar (but not identical) to this:

<audio controls preload="none" src="../../audio/windChimes.wav"></audio>

---

## Creating a pentatonic melody

The following program ([Ch. 6, p. 170](https://goo.gl/Y1VM5t)) **demonstrates how to harness randomness to create a melodic line within a particular scale.**

```python linenums="1" title="pentatonicMelody.py"
--8<-- "examples/_snippets/pentatonicMelody.py"
```

Since randomness is involved, it will generate output similar (but not identical) to this:

<audio controls preload="none" src="../../audio/pentatonicMelody.wav"></audio>

---

## Music from Brownian motion

Brownian motion is a very correlated, yet unpredictable (random) process observed commonly in nature. The following Python program **demonstrates how we can we harness randomness to generate music that is more correlated, “natural” sounding**.

```python linenums="1" title="brownianMelody.py"
--8<-- "examples/_snippets/brownianMelody.py"
```

Since randomness is involved, it will generate output similar (but not identical) to this:

<audio controls preload="none" src="../../audio/brownianMelody.wav"></audio>

---

## Throwing dice

The following program ([Ch. 6, p. 177](https://goo.gl/Y1VM5t)) **demonstrates how to simulate the throwing of dice** – how to divide randomness across many alternatives (in this case, 6).

```python linenums="1" title="throwingDice.py"
--8<-- "examples/_snippets/throwingDice.py"
```

Since randomness is involved, it will generate output similar (but not identical) to this:

<audio controls preload="none" src="../../audio/throwingDice.wav"></audio>

---

## Let the drums come alive

In the following program ([Ch. 6, p. 179](https://goo.gl/Y1VM5t)), **every now and then (randomly) we interject an open hi-hat sound to the sequence of closed hi-hat sounds**. It also randomly varies the loudness (dynamic level) of the notes.

```python linenums="1" title="drumsComeAlive.py"
--8<-- "examples/_snippets/drumsComeAlive.py"
```

Since randomness is involved, it will generate output similar (but not identical) to this:

<audio controls preload="none" src="../../audio/drumsComeAlive.wav"></audio>

---

## Creating generative music

Thee following program ([Ch. 6, p. 187](https://goo.gl/Y1VM5t)) **demonstrates how to develop more intricate algorithmic processes for **setting up probabilities of musical events (e.g., pitches and durations) and mapping them into** interesting musical artifacts**.

```python linenums="1" title="generativeMusic.py"
--8<-- "examples/_snippets/generativeMusic.py"
```

Since randomness is involved, it will generate output similar (but not identical) to this:

<audio controls preload="none" src="../../audio/generativeMusic.wav"></audio>
