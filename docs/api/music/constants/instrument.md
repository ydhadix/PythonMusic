# Instrument Constants

Instruments (also known as MIDI program changes) are represented as in the MIDI specification using integers from 0 to 127. That’s a total of 128 timbre settings.

The music library defines the following instrument constants for convenience:

| Constant | Value |
|---|---|
| `ACOUSTIC_GRAND`, `PIANO` | `0` |
| `BRIGHT_ACOUSTIC` | `1` |
| `ELECTRIC_GRAND` | `2` |
| `HONKYTONK_PIANO`, `HONKYTONK` | `3` |
| `EPIANO`, `EPIANO1`, `RHODES_PIANO`, `RHODES` | `4` |
| `EPIANO2`, `DX_PIANO`, `DX` | `5` |
| `HARPSICHORD` | `6` |
| `CLAVINET` | `7` |
| `CELESTA` | `8` |
| `GLOCKENSPIEL` | `9` |
| `MUSIC_BOX` | `10` |
| `VIBRAPHONE`, `VIBES` | `11` |
| `MARIMBA` | `12` |
| `XYLOPHONE` | `13` |
| `BELLS`, `TUBULAR_BELLS` | `14` |
| `DULCIMER` | `15` |
| `DRAWBAR_ORGAN`, `ORGAN` | `16` |
| `PERCUSSIVE_ORGAN`, `JAZZ_ORGAN` | `17` |
| `ROCK_ORGAN` | `18` |
| `CHURCH_ORGAN` | `19` |
| `REED_ORGAN` | `20` |
| `ACCORDION` | `21` |
| `HARMONICA` | `22` |
| `TANGO_ACCORDION`, `BANDONEON` | `23` |
| `NYLON_GUITAR`, `GUITAR` | `24` |
| `STEEL_GUITAR` | `25` |
| `JAZZ_GUITAR` | `26` |
| `CLEAN_GUITAR`, `ELECTRIC_GUITAR` | `27` |
| `MUTED_GUITAR` | `28` |
| `OVERDRIVE_GUITAR`, `OVERDRIVEN_GUITAR` | `29` |
| `DISTORTION_GUITAR` | `30` |
| `GUITAR_HARMONICS` | `31` |
| `ACOUSTIC_BASS` | `32` |
| `BASS`, `ELECTRIC_BASS`, `FINGERED_BASS` | `33` |
| `PICKED_BASS` | `34` |
| `FRETLESS_BASS` | `35` |
| `SLAP_BASS1` | `36` |
| `SLAP_BASS2` | `37` |
| `SYNTH_BASS1` | `38` |
| `SYNTH_BASS2` | `39` |
| `VIOLIN` | `40` |
| `VIOLA` | `41` |
| `CELLO` | `42` |
| `CONTRABASS` | `43` |
| `TREMOLO_STRINGS` | `44` |
| `PIZZICATO_STRINGS` | `45` |
| `ORCHESTRAL_HARP`, `HARP` | `46` |
| `TIMPANI` | `47` |
| `STRING_ENSEMBLE1`, `STRINGS` | `48` |
| `STRING_ENSEMBLE2` | `49` |
| `SYNTH_STRINGS1`, `SYNTH` | `50` |
| `SYNTH_STRINGS2` | `51` |
| `CHOIR_AHHS`, `CHOIR` | `52` |
| `VOICE_OOHS`, `VOICE` | `53` |
| `SYNTH_VOICE`, `VOX` | `54` |
| `ORCHESTRA_HIT` | `55` |
| `TRUMPET` | `56` |
| `TROMBONE` | `57` |
| `TUBA` | `58` |
| `MUTED_TRUMPET` | `59` |
| `FRENCH_HORN`, `HORN` | `60` |
| `BRASS_SECTION`, `BRASS` | `61` |
| `SYNTH_BRASS1` | `62` |
| `SYNTH_BRASS2` | `63` |
| `SOPRANO_SAX`, `SOPRANO_SAXOPHONE` | `64` |
| `ALTO_SAX`, `ALTO_SAXOPHONE` | `65` |
| `TENOR_SAX`, `TENOR_SAXOPHONE`, `SAX`, `SAXOPHONE` | `66` |
| `BARITONE_SAX`, `BARITONE_SAXOPHONE` | `67` |
| `OBOE` | `68` |
| `ENGLISH_HORN` | `69` |
| `BASSOON` | `70` |
| `CLARINET` | `71` |
| `PICCOLO` | `72` |
| `FLUTE` | `73` |
| `RECORDER` | `74` |
| `PAN_FLUTE` | `75` |
| `BLOWN_BOTTLE`, `BOTTLE` | `76` |
| `SHAKUHACHI` | `77` |
| `WHISTLE` | `78` |
| `OCARINA` | `79` |
| `LEAD_1_SQUARE`, `SQUARE` | `80` |
| `LEAD_2_SAWTOOTH`, `SAWTOOTH` | `81` |
| `LEAD_3_CALLIOPE`, `CALLIOPE` | `82` |
| `LEAD_4_CHIFF`, `CHIFF` | `83` |
| `LEAD_5_CHARANG`, `CHARANG` | `84` |
| `LEAD_6_VOICE`, `SOLO_VOX` | `85` |
| `LEAD_7_FIFTHS`, `FIFTHS` | `86` |
| `LEAD_8_BASS_LEAD`, `BASS_LEAD` | `87` |
| `PAD_1_NEW_AGE`, `NEW_AGE` | `88` |
| `PAD_2_WARM`, `WARM_PAD` | `89` |
| `PAD_3_POLYSYNTH`, `POLYSYNTH` | `90` |
| `PAD_4_CHOIR`, `SPACE_VOICE` | `91` |
| `PAD_5_GLASS`, `BOWED_GLASS` | `92` |
| `PAD_6_METTALIC`, `METALLIC` | `93` |
| `PAD_7_HALO` | `94` |
| `PAD_8_SWEEP` | `95` |
| `FX_1_RAIN`, `ICE_RAIN` | `96` |
| `FX_2_SOUNDTRACK` | `97` |
| `FX_3_CRYSTAL` | `98` |
| `FX_4_ATMOSPHERE` | `99` |
| `FX_5_BRIGHTNESS`, `BRIGHTNESS` | `100` |
| `FX_6_GOBLINS`, `GOBLINS` | `101` |
| `FX_7_ECHOES`, `ECHO_DROPS` | `102` |
| `FX_8_SCI_FI`, `SCI_FI` | `103` |
| `SITAR` | `104` |
| `BANJO` | `105` |
| `SHAMISEN` | `106` |
| `KOTO` | `107` |
| `KALIMBA` | `108` |
| `BAGPIPE` | `109` |
| `FIDDLE` | `110` |
| `SHANNAI` | `111` |
| `TINKLE_BELL`, `BELL` | `112` |
| `AGOGO` | `113` |
| `STEEL_DRUMS` | `114` |
| `WOODBLOCK` | `115` |
| `TAIKO_DRUM`, `TAIKO` | `116` |
| `MELODIC_TOM`, `TOM_TOM` | `117` |
| `SYNTH_DRUM` | `118` |
| `REVERSE_CYMBAL` | `119` |
| `GUITAR_FRET_NOISE`, `FRET_NOISE` | `120` |
| `BREATH_NOISE`, `BREATHNOISE`, `BREATH` | `121` |
| `SEASHORE`, `SEA` | `122` |
| `BIRD_TWEET`, `BIRD` | `123` |
| `TELEPHONE_RING`, `TELEPHONE` | `124` |
| `HELICOPTER` | `125` |
| `APPLAUSE` | `126` |
| `GUNSHOT` | `127` |