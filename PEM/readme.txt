CREATIVEPYTHON

This folder contains the necessary files to:
	- Install PythonMusic via pip (soon to be 'JythonMusic')
	- Test and update the PEM editor
	- Build an executable of PEM, with dependencies included

### Installing PythonMusic
1. Open a terminal in this directory.
2. Run "pip install ."
3. PythonMusic, and its dependencies, will be installed from the local 'src' directory.

Notes:
	- You can add -e to the pip install command for testing/debugging.  Changes made to the src folder will be reflected in your PythonMusic installation.


### Running the PEM editor
1. Open a terminal in the PEM directory.
2. Run "python PEM.py"
3. When PEM starts, it will open an editor window.

Notes:
	- PEM doesn't require any additional installations.
	- When run directly, PEM uses your current Python environment, and only has access to currently installed libraries.
	- PEM.py, pemlib/, and icons/ are PEM sources;
		build.py, hook/, and the .sf2 are part of PyInstaller (below)


### Building PEM executables with PyInstaller
1. Open a terminal in the PEM directory.
2. Run "python build.py"
	a. add "--include-soundfont" to bundle a .sf2 with the executable.
		- This increases the file size and may slow down load times,
		  but allows PEM to be completely portable.
3. A PEM executable (.exe or .app) will be output in a newly created PEM/dist directory

Notes:
	- You don't need to have PyInstaller or PythonMusic installed to build the PEM executable.  The build script creates a clean, local python environment, installs PyInstaller, PythonMusic and its dependencies there, and uses that to build the executable.  (Your normal python installations won't be changed.)