# PythonMusic

PythonMusic is a Python-based software environment for learning and developing algorithmic art projects. It mirrors the [JythonMusic API](https://jythonmusic.me/api-reference/).

**Full documentation, tutorials, and examples live at [pythonmusic.org](https://pythonmusic.org/).** This README covers only the essentials.

## Installation

Requires **Python 3.12+** and a **C++ compiler** (some dependencies build native code). On Linux, install [portaudio](http://portaudio.com/) first.

```
# Windows/macOS
pip install PythonMusic

# Linux (Debian/Ubuntu)
sudo apt-get install portaudio19-dev
pip install PythonMusic
```

If installation fails for lack of a compiler, install the [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) (Windows) or [Xcode](https://apps.apple.com/us/app/xcode/id497799835?mt=12) (macOS), then retry. See the [site](https://pythonmusic.org/) for full setup help.

The first time you `import music`, PythonMusic offers to download a default soundfont (FluidR3 GM) to a local cache for MIDI playback.

## PEM editor

PythonMusic ships with PEM, a customized Python editor (a hard fork of IDLE). After installing, run:

```
pem <filename.py>
```

## License

PythonMusic and PEM are free software under the [GNU GPL v3 or later](https://www.gnu.org/licenses/gpl-3.0.html) (see `LICENSE`). PythonMusic derives from [JythonMusic](https://jythonmusic.me/), which is also GPLv3.

- PEM's IDLE-derived components remain under the Python Software Foundation License v2 (`LICENSE-PSF`).
- The bundled `nevmuse` metrics component is a separate work with its own terms (see `src/PythonMusic/nevmuse/NOTICE.txt`).

For full licensing details, see `LICENSE` and `LICENSE-PSF`.
