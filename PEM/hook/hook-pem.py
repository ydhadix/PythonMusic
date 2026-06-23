# PyInstaller hook for pem
# This hook tells PyInstaller how to properly collect pem and its dependencies

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all pem submodules
hiddenimports = collect_submodules('pem')

# Also ensure critical standard library dependencies are included
# These are dependencies that pem uses but PyInstaller might not detect
hiddenimports += [
   'html',
   'html.parser',
   'html.entities',
   'tkinter',
   'tkinter.font',
   'tkinter.messagebox',
   'tkinter.ttk',
   'tkinter.constants',
   'tkinter.filedialog',
   'tkinter.simpledialog',
   'tkinter.colorchooser',
   'tkinter.commondialog',
   'tkinter.dialog',
]

# Collect all data files from pem (config files, icons, help files, etc.)
datas = collect_data_files('pem', include_py_files=True)
