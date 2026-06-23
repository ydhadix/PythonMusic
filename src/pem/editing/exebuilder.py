"""Build a standalone executable from the current editor script (PyInstaller).

WORK IN PROGRESS -- the "Create Executable" feature is not currently functional,
which is why its menu item / toolbar button are disabled.  The code is kept here
for a future fix; fixing it is out of scope for the 2025-26 refactor.  Build
options (what to bundle / exclude) come from PEM/packages.py.
"""

import sys
import os
import tempfile
import shutil
import platform
import threading
from pathlib import Path
from tkinter import messagebox
from tkinter import Toplevel, Label, StringVar
from tkinter.ttk import Progressbar


class ExeBuilder:
   """Handles creation of PyInstaller executables from user scripts"""

   def __init__(self, editwin):
      """Initialize with reference to editor window

      Args:
         editwin: EditorWindow instance with io.filename and io.save() method
      """
      self.editwin = editwin
      self.scriptPath = None
      self.scriptDir = None
      self.scriptName = None
      self.tempDir = None

   def create_executable(self):
      """Main entry point for creating executable"""
      # Step 1: Auto-save file if needed
      if not self._ensure_file_saved():
         return

      # Step 2: Show confirmation dialog
      if not self._confirm_build():
         return

      # Step 3: Check PyInstaller availability
      if not self._check_pyinstaller():
         return

      # Step 4: Create progress dialog (modal/blocking)
      progressDialog = ProgressDialog(self.editwin.top)

      # Step 5: Build executable in blocking mode
      success, exePath = self._build_executable(progressDialog)

      # Step 6: Close progress dialog
      progressDialog.close()

      # Step 7: Show result
      if success:
         self._show_success(exePath)
      else:
         self._show_error()

   def _ensure_file_saved(self):
      """Ensure file is saved and get script path

      Returns:
         bool: True if file is saved, False if user cancels
      """
      filename = self.editwin.io.filename

      # if no filename, prompt for save
      if not filename:
         # trigger save dialog
         self.editwin.io.save(None)
         filename = self.editwin.io.filename

         # user canceled save dialog
         if not filename:
            return False

      # if file has unsaved changes, auto-save
      if not self.editwin.get_saved():
         self.editwin.io.save(None)

      # store script info
      self.scriptPath = Path(filename).resolve()
      self.scriptDir = self.scriptPath.parent
      self.scriptName = self.scriptPath.stem

      return True

   def _confirm_build(self):
      """Show confirmation dialog

      Returns:
         bool: True if user confirms, False if user cancels
      """
      # determine executable name based on platform
      system = platform.system()
      exeName = self.scriptName + ('.exe' if system == 'Windows' else '')

      message = (
         f"Create executable for {self.scriptPath.name}?\n\n"
         f"This will create {exeName} in the same directory as your script.\n"
         f"The process may take a few minutes."
      )

      result = messagebox.askyesno(
         title="Create Executable",
         message=message,
         parent=self.editwin.text
      )

      return result

   def _check_pyinstaller(self):
      """Verify PyInstaller is installed

      Returns:
         bool: True if available, False otherwise
      """
      try:
         import PyInstaller
         return True
      except ImportError:
         message = (
            "PyInstaller is required to create executables.\n\n"
            "Install it with:\n"
            "pip install pyinstaller"
         )
         messagebox.showerror(
            title="PyInstaller Not Found",
            message=message,
            parent=self.editwin.text
         )
         return False

   def _build_executable(self, progressDialog):
      """Run PyInstaller and build executable

      Args:
         progressDialog: ProgressDialog instance for status updates

      Returns:
         tuple: (success: bool, exePath: str or None)
      """
      import PyInstaller.__main__

      # create temp directory for build artifacts
      self.tempDir = Path(tempfile.mkdtemp(prefix='pem_build_'))

      try:
         progressDialog.update_status("Analyzing dependencies...")

         # determine executable name based on platform
         system = platform.system()
         exeName = self.scriptName + ('.exe' if system == 'Windows' else '')
         exePath = self.scriptDir / exeName

         # find PythonMusic source directory
         creativePythonSrc = self._find_creativepython_src()

         # create interactive wrapper script that runs user's script in interactive mode
         wrapperPath = self._create_interactive_wrapper()

         # build PyInstaller command with minimal hidden imports
         command = [
            '--onefile',                           # single executable
            '--console',   # always show console for visibility and debugging
            '--clean',                             # clean cache
            '--name', self.scriptName,             # output name
            '--distpath', str(self.scriptDir),     # output to script directory
            '--workpath', str(self.tempDir / 'build'),   # temp build folder
            '--specpath', str(self.tempDir),       # temp spec folder
            '--add-data', f'{self.scriptPath}{os.pathsep}.',  # bundle user's script
         ]

         # find and bundle local Python modules and packages that the script imports
         localModules = self._find_local_modules()
         for modulePath, isPackage in localModules:
            if isPackage:
               # for packages, preserve directory structure
               # format: 'source_dir{sep}destination_dir'
               packageName = modulePath.name
               command.extend(['--add-data', f'{modulePath}{os.pathsep}{packageName}'])
            else:
               # for single .py files, add to root
               command.extend(['--add-data', f'{modulePath}{os.pathsep}.'])

         # add PythonMusic src to search paths if found
         if creativePythonSrc:
            command.extend(['--paths', str(creativePythonSrc)])

         # add bundled standard library to search paths if frozen
         if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            stdlibPath = Path(sys._MEIPASS) / 'python_lib'
            if stdlibPath.exists():
               command.extend(['--paths', str(stdlibPath)])

         # analyze user's script to find which modules they actually import
         userImports = self._analyze_script_imports()

         # add hidden imports for modules PyInstaller commonly misses
         hidden_imports = [
            'tinysoundfont',
            'sounddevice',
         ]

         # add only the PythonMusic modules that the user actually imports
         creativepython_modules = ['music', 'gui', 'timer', 'osc', 'midi', 'image', 'markov', 'zipf', 'iannix']
         for module in creativepython_modules:
            if module in userImports:
               hidden_imports.append(module)

         for module in hidden_imports:
            command.extend(['--hidden-import', module])

         # get exclusions from the build configuration, if available.
         # ``packages`` is build-only tooling (it lives in the PEM/ build folder,
         # not in the shipped package), so a pip install won't have it -- in that
         # case fall back to no extra exclusions rather than failing.
         try:
            import packages
            all_excludes = packages.getExcludes(profile='user_script')
         except ImportError:
            all_excludes = []

         for module in all_excludes:
            command.extend(['--exclude-module', module])

         # add the wrapper as entry point
         command.append(str(wrapperPath))

         progressDialog.update_status("Creating Executable...")

         # run PyInstaller in a separate thread to keep UI responsive
         build_success = [False]   # use list to allow modification in thread
         build_error = [None]

         def run_pyinstaller():
            """Run PyInstaller in background thread"""
            try:
               PyInstaller.__main__.run(command)
               build_success[0] = True
            except Exception as e:
               build_error[0] = e

         # start build thread
         build_thread = threading.Thread(target=run_pyinstaller, daemon=True)
         build_thread.start()

         # keep UI responsive while build runs
         while build_thread.is_alive():
            progressDialog.dialog.update()
            build_thread.join(timeout=0.1)   # check every 100ms

         # check for errors
         if build_error[0]:
            raise build_error[0]

         # check if executable was created
         if exePath.exists():
            progressDialog.update_status("Cleaning up...")

            # clean up temp files
            try:
               if self.tempDir and self.tempDir.exists():
                  shutil.rmtree(str(self.tempDir))
            except Exception as e:
               # log but don't fail - cleanup not critical
               print(f"Warning: Failed to clean up temp files: {e}")

            return True, str(exePath)
         else:
            return False, None

      except Exception as e:
         print(f"Build error: {e}")
         return False, None

   def _find_creativepython_src(self):
      """Find PythonMusic source directory

      Returns:
         Path or None: Path to src directory if found
      """
      # try common locations relative to PEM (this module is in
      # pem/editing/, so go up: editing -> pem -> PEM -> repo)
      candidates = [
         Path(__file__).parent.parent.parent.parent / 'src',  # repo root
         Path(__file__).parent.parent.parent / 'src',         # PEM dir
         Path.cwd() / 'src',                                   # current directory
      ]

      # also check if running from installed package
      try:
         import music
         if hasattr(music, '__file__'):
            musicPath = Path(music.__file__).parent
            candidates.append(musicPath)
      except ImportError:
         pass

      for candidate in candidates:
         if candidate.exists() and candidate.is_dir():
            # verify it's the right directory by checking for key modules
            if (candidate / 'music.py').exists() or (candidate / 'osc.py').exists():
               return candidate

      return None

   def _analyze_script_imports(self):
      """Analyze user's script to find imported modules

      Returns:
         set: Set of module names imported by the script
      """
      import ast
      import re

      imports = set()

      try:
         # read the user's script
         with open(self.scriptPath, 'r', encoding='utf-8') as f:
            scriptContent = f.read()

         # parse with AST for proper Python parsing
         try:
            tree = ast.parse(scriptContent)

            for node in ast.walk(tree):
               # handle "import module"
               if isinstance(node, ast.Import):
                  for alias in node.names:
                     imports.add(alias.name.split('.')[0])  # get top-level module

               # handle "from module import ..."
               elif isinstance(node, ast.ImportFrom):
                  if node.module:
                     imports.add(node.module.split('.')[0])  # get top-level module

         except SyntaxError:
            # if AST parsing fails, fall back to regex (less accurate but better than nothing)
            import_patterns = [
               r'^\s*import\s+(\w+)',              # import module
               r'^\s*from\s+(\w+)\s+import',       # from module import
            ]

            for line in scriptContent.split('\n'):
               for pattern in import_patterns:
                  match = re.match(pattern, line)
                  if match:
                     imports.add(match.group(1))

      except Exception as e:
         print(f"Warning: Could not analyze script imports: {e}")

      return imports

   def _find_local_modules(self):
      """Find local Python modules and packages in the script's directory that are imported

      Returns:
         list: List of tuples (Path, is_package) for local modules/packages to bundle
               is_package=True means it's a directory package, False means single .py file
      """
      import ast

      local_modules = []

      try:
         # read the user's script
         with open(self.scriptPath, 'r', encoding='utf-8') as f:
            scriptContent = f.read()

         # parse with AST to find imports
         tree = ast.parse(scriptContent)
         imported_names = set()

         for node in ast.walk(tree):
            # handle "import module" or "import package.module"
            if isinstance(node, ast.Import):
               for alias in node.names:
                  imported_names.add(alias.name.split('.')[0])

            # handle "from module import ..." or "from package.module import ..."
            elif isinstance(node, ast.ImportFrom):
               if node.module and node.level == 0:  # absolute imports only
                  imported_names.add(node.module.split('.')[0])

         # check which imports correspond to local files or packages
         for name in imported_names:
            # check for package (directory with __init__.py)
            potential_package = self.scriptDir / name
            if potential_package.is_dir() and (potential_package / '__init__.py').exists():
               local_modules.append((potential_package, True))  # it's a package
               continue

            # check for single .py file
            potential_file = self.scriptDir / f"{name}.py"
            if potential_file.exists() and potential_file != self.scriptPath:
               local_modules.append((potential_file, False))  # it's a single module

      except Exception as e:
         print(f"Warning: Could not analyze local modules: {e}")

      return local_modules

   def _create_interactive_wrapper(self):
      """Create wrapper script that runs user's script in interactive mode

      This wrapper simulates 'python -i script.py' behavior by:
      1. Executing the user's script in __main__ namespace
      2. Starting an interactive REPL to keep the program alive

      This is necessary for PythonMusic programs that:
      - Use GUI (need QApplication event loop running)
      - Play music (need time for audio playback)
      - Use timers (need event loop for animations)

      Returns:
         Path: Path to wrapper script
      """
      wrapperPath = self.tempDir / '_interactive_wrapper.py'

      # get the script filename for bundling
      scriptFilename = self.scriptPath.name

      wrapperContent = f'''#!/usr/bin/env python3
"""Interactive wrapper for PythonMusic executable"""

import sys
import os
import code

def main():
   """Run user script in interactive mode (simulates python -i)"""

   # determine script location (bundled with PyInstaller)
   if getattr(sys, 'frozen', False):
      # running in PyInstaller bundle
      if hasattr(sys, '_MEIPASS'):
         script_path = os.path.join(sys._MEIPASS, {scriptFilename!r})
      else:
         script_path = os.path.join(os.path.dirname(sys.executable), {scriptFilename!r})
   else:
      # running in development
      script_path = {scriptFilename!r}

   # set up __main__ namespace for script execution
   import __main__
   __main__.__file__ = script_path

   # change to script directory so relative imports work
   script_dir = os.path.dirname(os.path.abspath(script_path))
   if script_dir:
      os.chdir(script_dir)
      # add script directory to Python path for local module imports
      if script_dir not in sys.path:
         sys.path.insert(0, script_dir)

   # read and compile the user's script
   try:
      with open(script_path, 'r', encoding='utf-8') as f:
         script_code = f.read()
   except Exception as e:
      print(f"Error reading script: {{e}}")
      input("Press Enter to exit...")
      return

   try:
      compiled_code = compile(script_code, script_path, 'exec')
   except SyntaxError as e:
      print(f"Syntax error in script: {{e}}")
      input("Press Enter to exit...")
      return

   # execute the script in __main__ namespace
   try:
      exec(compiled_code, vars(__main__))
   except SystemExit:
      # script called exit() - respect it but still enter interactive mode
      pass
   except Exception as e:
      import traceback
      print()
      print("=" * 60)
      print("Exception occurred during script execution:")
      print("=" * 60)
      traceback.print_exc()
      print("=" * 60)

   # enter interactive mode to keep program alive (for GUI, music, timers, etc.)
   # user can inspect variables, run commands, or type exit() to quit
   try:
      code.interact(local=vars(__main__), banner="", exitmsg="")
   except (EOFError, KeyboardInterrupt):
      # user pressed Ctrl+Z or Ctrl+C - exit gracefully
      pass

if __name__ == '__main__':
   main()
'''
      wrapperPath.write_text(wrapperContent, encoding='utf-8')
      return wrapperPath

   def _show_success(self, exePath):
      """Show success message

      Args:
         exePath: Path to created executable
      """
      message = (
         f"Successfully created executable:\n\n"
         f"{exePath}\n\n"
         f"You can share this file with others on the same platform."
      )
      messagebox.showinfo(
         title="Executable Created",
         message=message,
         parent=self.editwin.text
      )

   def _show_error(self):
      """Show error message"""
      message = (
         "Failed to create executable.\n\n"
         "Check that all required packages are installed.\n"
         "See the console for error details."
      )
      messagebox.showerror(
         title="Build Failed",
         message=message,
         parent=self.editwin.text
      )


class ProgressDialog:
   """Modal progress dialog for blocking UI during build"""

   def __init__(self, parent):
      """Create progress dialog

      Args:
         parent: Parent window
      """
      self.dialog = Toplevel(parent)
      self.dialog.title("Creating Executable")
      self.dialog.geometry("400x150")
      self.dialog.resizable(False, False)

      # make modal
      self.dialog.transient(parent)
      self.dialog.grab_set()

      # center on parent
      self.dialog.update_idletasks()
      x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
      y = parent.winfo_y() + (parent.winfo_height() // 2) - 75
      self.dialog.geometry(f"+{x}+{y}")

      # status label
      self.statusVar = StringVar(master=self.dialog, value="Preparing build...")
      statusLabel = Label(self.dialog, textvariable=self.statusVar,
                         wraplength=350)
      statusLabel.pack(pady=(20, 10))

      # indeterminate progress bar
      self.progress = Progressbar(self.dialog, mode='indeterminate',
                                 length=350)
      self.progress.pack(pady=10)
      self.progress.start(10)

      # force update
      self.dialog.update()

   def update_status(self, message):
      """Update status message

      Args:
         message: New status message to display
      """
      self.statusVar.set(message)
      self.dialog.update()

   def close(self):
      """Close progress dialog"""
      self.progress.stop()
      self.dialog.grab_release()
      self.dialog.destroy()
