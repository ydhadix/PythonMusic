"""
Pemlib objects with no external pem dependencies
which are needed in more than one pem module.

They are included here because
    a) they don't particularly belong elsewhere; or
    b) because inclusion here simplifies the pem dependency graph.

TODO:
    * Python versions (editor and help_about),
    * tk version and patchlevel (pyshell, help_about, maxos?, editor?),
    * std streams (pyshell, run),
    * warning stuff (pyshell, run).
"""
import sys

# .pyw is for Windows; .pyi is for typing stub files.
# The extension order is needed for iomenu open/save dialogs.
py_extensions = ('.py', '.pyw', '.pyi')


# Cursor to show over clickable links. Tk's portable 'hand2' renders as a
# dated bitmap hand on macOS, so use the native Cocoa 'pointinghand' there;
# 'hand2' is the conventional, native-looking link cursor everywhere else.
# Use this anywhere PEM makes text clickable so the hand looks right per OS.
if sys.platform == 'darwin':
    LINK_CURSOR = 'pointinghand'
else:
    LINK_CURSOR = 'hand2'


# Fix for HiDPI screens on Windows.  CALL BEFORE ANY TK OPERATIONS!
# URL for arguments for the ...Awareness call below.
# https://msdn.microsoft.com/en-us/library/windows/desktop/dn280512(v=vs.85).aspx
if sys.platform == 'win32':  # pragma: no cover
    def fix_win_hidpi():  # Called in pyshell and turtledemo.
        try:
            import ctypes
            PROCESS_SYSTEM_DPI_AWARE = 1  # Int required.
            ctypes.OleDLL('shcore').SetProcessDpiAwareness(PROCESS_SYSTEM_DPI_AWARE)
        except (ImportError, AttributeError, OSError):
            pass

    def set_win_app_id(app_id):  # Called in pyshell.
        """Tell Windows this process is its own app, not 'python'.

        Without this, PEM's windows inherit python.exe's taskbar identity, so
        they group under a Python icon labelled 'python'. Setting an explicit
        AppUserModelID makes Windows treat PEM as a distinct app, grouping its
        windows together under PEM's own icon. Call once, before any window is
        created.
        """
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except (ImportError, AttributeError, OSError):
            pass


def fix_scaling(root):
    """Scale Tk's named fonts down on HiDPI displays so the GUI isn't oversized.

    Call once after creating the Tk root.  ``import tkinter.font`` is local so
    this module stays import-light for callers that don't need it.
    """
    import tkinter.font
    scaling = float(root.tk.call('tk', 'scaling'))
    if scaling > 1.4:
        for name in tkinter.font.names(root):
            font = tkinter.font.Font(root=root, name=name, exists=True)
            size = int(font['size'])
            if size < 0:
                font['size'] = round(-0.75 * size)


if __name__ == '__main__':
    from unittest import main
    main('pem.pem_test.test_util', verbosity=2)
