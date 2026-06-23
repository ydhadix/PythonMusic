# Pitch Constants

Note pitches are represented as in the MIDI specification, using integers from 0 (lowest pitch) to 127 (highest pitch). That’s a total of 128 pitches (i.e., 10 octaves).

The music library defines the following pitch constants for convenience.

First, there is a special pitch `REST` corresponding to rests.

Rests are notes that last as long as you specify (see [duration constants](duration.md)), but produce no sound.

The lowest possible note is `C_1` (C negative one); it is equal to 0.  The highest possible pitch is `G9`; it is equal to 127. 

| Constant | Value |
|---|---|
| `C_1` | `0` |
| `CS_1`, `DF_1` | `1` |
| `D_1` | `2` |
| `EF_1`, `DS_1` | `3` |
| `E_1`, `FF_1` | `4` |
| `F_1`, `ES_1` | `5` |
| `FS_1`, `GF_1` | `6` |
| `G_1` | `7` |
| `AF_1`, `GS_1` | `8` |
| `A_1` | `9` |
| `BF_1`, `AS_1` | `10` |
| `B_1`, `CF0` | `11` |
| `C0`, `BS_1` | `12` |
| `CS0`, `DF0` | `13` |
| `D0` | `14` |
| `EF0`, `DS0` | `15` |
| `E0`, `FF0` | `16` |
| `F0`, `ES0` | `17` |
| `FS0`, `GF0` | `18` |
| `G0` | `19` |
| `AF0`, `GS0` | `20` |
| `A0` | `21` |
| `BF0`, `AS0` | `22` |
| `B0`, `CF1` | `23` |
| `C1`, `BS0` | `24` |
| `CS1`, `DF1` | `25` |
| `D1` | `26` |
| `EF1`, `DS1` | `27` |
| `E1`, `FF1` | `28` |
| `F1`, `ES1` | `29` |
| `FS1`, `GF1` | `30` |
| `G1` | `31` |
| `AF1`, `GS1` | `32` |
| `A1` | `33` |
| `BF1`, `AS1` | `34` |
| `B1`, `CF2` | `35` |
| `C2`, `BS1` | `36` |
| `CS2`, `DF2` | `37` |
| `D2` | `38` |
| `EF2`, `DS2` | `39` |
| `E2`, `FF2` | `40` |
| `F2`, `ES2` | `41` |
| `FS2`, `GF2` | `42` |
| `G2` | `43` |
| `AF2`, `GS2` | `44` |
| `A2` | `45` |
| `BF2`, `AS2` | `46` |
| `B2`, `CF3` | `47` |
| `C3`, `BS2` | `48` |
| `CS3`, `DF3` | `49` |
| `D3` | `50` |
| `EF3`, `DS3` | `51` |
| `E3`, `FF3` | `52` |
| `F3`, `ES3` | `53` |
| `FS3`, `GF3` | `54` |
| `G3` | `55` |
| `AF3`, `GS3` | `56` |
| `A3` | `57` |
| `BF3`, `AS3` | `58` |
| `B3`, `CF4` | `59` |
| `C4`, `BS3` | `60` |
| `CS4`, `DF4` | `61` |
| `D4` | `62` |
| `EF4`, `DS4` | `63` |
| `E4`, `FF4` | `64` |
| `F4`, `ES4` | `65` |
| `FS4`, `GF4` | `66` |
| `G4` | `67` |
| `AF4`, `GS4` | `68` |
| `A4` | `69` |
| `BF4`, `AS4` | `70` |
| `B4`, `CF5` | `71` |
| `C5`, `BS4` | `72` |
| `CS5`, `DF5` | `73` |
| `D5` | `74` |
| `EF5`, `DS5` | `75` |
| `E5`, `FF5` | `76` |
| `F5`, `ES5` | `77` |
| `FS5`, `GF5` | `78` |
| `G5` | `79` |
| `AF5`, `GS5` | `80` |
| `A5` | `81` |
| `BF5`, `AS5` | `82` |
| `B5`, `CF6` | `83` |
| `C6`, `BS5` | `84` |
| `CS6`, `DF6` | `85` |
| `D6` | `86` |
| `EF6`, `DS6` | `87` |
| `E6`, `FF6` | `88` |
| `F6`, `ES6` | `89` |
| `FS6`, `GF6` | `90` |
| `G6` | `91` |
| `AF6`, `GS6` | `92` |
| `A6` | `93` |
| `BF6`, `AS6` | `94` |
| `B6`, `CF7` | `95` |
| `C7`, `BS6` | `96` |
| `CS7`, `DF7` | `97` |
| `D7` | `98` |
| `EF7`, `DS7` | `99` |
| `E7`, `FF7` | `100` |
| `F7`, `ES7` | `101` |
| `FS7`, `GF7` | `102` |
| `G7` | `103` |
| `AF7`, `GS7` | `104` |
| `A7` | `105` |
| `BF7`, `AS7` | `106` |
| `B7`, `CF8` | `107` |
| `C8`, `BS7` | `108` |
| `CS8`, `DF8` | `109` |
| `D8` | `110` |
| `EF8`, `DS8` | `111` |
| `E8`, `FF8` | `112` |
| `F8`, `ES8` | `113` |
| `FS8`, `GF8` | `114` |
| `G8` | `115` |
| `AF8`, `GS8` | `116` |
| `A8` | `117` |
| `BF8`, `AS8` | `118` |
| `B8`, `CF9` | `119` |
| `C9`, `BS8` | `120` |
| `CS9`, `DF9` | `121` |
| `D9` | `122` |
| `EF9`, `DS9` | `123` |
| `E9`, `FF9` | `124` |
| `F9`, `ES9` | `125` |
| `FS9`, `GF9` | `126` |
| `G9` | `127` |