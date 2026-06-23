"""Console entry point for PEM, the PythonMusic IDE.

Run via the ``pem`` command or ``python -m pem``.  Opens the editor, optionally
on a file given on the command line or by drag-and-drop.

The PyInstaller-frozen build uses a separate entry (``PEM/PEM.py``) that adds
the bundle-specific bootstrap and then delegates back here.
"""

import sys
import os

PEM_APP_NAME = "PEM"


def launchEditor(filePath=None):
    """Launch the PEM editor GUI, optionally opening ``filePath``."""
    originalArgv = sys.argv[:]
    try:
        from pem import pyshell
        pemArgs = [PEM_APP_NAME, '-e']  # -e: open an editor window, no shell
        if filePath and os.path.exists(filePath):
            pemArgs.append(os.path.abspath(filePath))
        sys.argv = pemArgs
        pyshell.main()
    finally:
        sys.argv = originalArgv


def main():
    """Open the editor, optionally on a file given as the first argument."""
    if len(sys.argv) >= 2:
        targetFile = sys.argv[1]
        if os.path.exists(targetFile):
            launchEditor(targetFile)
        else:
            print(f"Error: Could not find file {targetFile}")
            sys.exit(1)
    else:
        launchEditor()


if __name__ == "__main__":
    main()
