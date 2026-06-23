# This file is part of PythonMusic.
#
# PythonMusic is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.  PythonMusic is distributed WITHOUT ANY WARRANTY.  See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
#
# PythonMusic derives from JythonMusic (https://jythonmusic.me),
# Copyright (C) 2011-2023 Bill Manaris et al.
# Modifications Copyright (C) 2025 Dr. Bill Manaris and the PythonMusic contributors.

import sys, platform, ctypes, importlib, importlib.resources
from importlib.metadata import version as _metadata_version

try:
    __version__ = _metadata_version("PythonMusic")
except Exception:
    __version__ = "unknown"


# Preload the bundled portaudio binary on macOS.
#
# pyaudio (pulled in by tinysoundfont's synth) ships a compiled extension whose
# dependent-library load command points at a hardcoded Homebrew path
# (/opt/homebrew/.../libportaudio.2.dylib).  Without Homebrew that dlopen fails.
# Our bundled dylib carries that exact install name, so loading it here registers
# the image with dyld; pyaudio's later dlopen then resolves to the already-loaded
# image instead of touching the filesystem path.  This must run before pyaudio is
# imported (i.e. before the synth starts).
if platform.system() == "Darwin":
   try:
      _libpath = importlib.resources.files("PythonMusic") / "bin" / "libportaudio.2.dylib"
      ctypes.CDLL(str(_libpath))
   except Exception:
      pass


# The library modules (music, gui, midi, ...) are installed as top-level
# modules, sitting beside this package rather than inside it.  Re-export them
# here so both import styles work and refer to the exact same module objects:
#
#     from music import *           # bare
#     from PythonMusic import music # namespaced
#
# This must match the py-modules list in pyproject.toml.
_LIBRARY_MODULES = {
   "gui", "image", "midi", "music", "osc",
   "timer", "iannix", "markov", "zipf", "utilities",
}


def __getattr__(name):
   # Called only when "name" isn't already an attribute of this package, so
   # each library module is imported the first time it is actually requested
   # (e.g. on "from PythonMusic import music"), not when PythonMusic loads.
   if name in _LIBRARY_MODULES:
      module = importlib.import_module(name)
      # Cache it as both PythonMusic.<name> and a real submodule entry so the
      # next lookup skips this function and "import PythonMusic.music" works too.
      setattr(sys.modules[__name__], name, module)
      sys.modules[f"{__name__}.{name}"] = module
      return module
   raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
   # Makes the library modules show up in tab-completion and dir(PythonMusic).
   return sorted(set(globals()) | _LIBRARY_MODULES)
