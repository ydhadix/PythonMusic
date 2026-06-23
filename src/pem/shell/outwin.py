"""Editor window that can serve as an output file.
"""

import re

from tkinter import messagebox

from pem.editing.editor import EditorWindow


file_line_pats = [
    # order of patterns matters
    r'file "([^"]*)", line (\d+)',
    r'([^\s]+)\((\d+)\)',
    r'^(\s*\S.*?):\s*(\d+):',  # Win filename, maybe starting with spaces
    r'([^\s]+):\s*(\d+):',     # filename or path, ltrim
    r'^\s*(\S.*?):\s*(\d+):',  # Win abs path with embedded spaces, ltrim
]

file_line_progs = None


def compile_progs():
    "Compile the patterns for matching to file name and line number."
    global file_line_progs
    file_line_progs = [re.compile(pat, re.IGNORECASE)
                       for pat in file_line_pats]


def file_line_helper(line):
    """Extract file name and line number from line of text.

    Check if line of text contains one of the file/line patterns.
    If it does and if the file and line are valid, return
    a tuple of the file name and line number.  If it doesn't match
    or if the file or line is invalid, return None.
    """
    if not file_line_progs:
        compile_progs()
    for prog in file_line_progs:
        match = prog.search(line)
        if match:
            filename, lineno = match.group(1, 2)
            try:
                f = open(filename)
                f.close()
                break
            except OSError:
                continue
    else:
        return None
    try:
        return filename, int(lineno)
    except TypeError:
        return None


class OutputWindow(EditorWindow):
    """An editor window that doubles as a write-only output file.

    Also the base class of the Console window (PyShell).  Adds the
    "open the file at this line" binding for "File ..., line N" output, and a
    write()/writelines()/flush() trio so it can stand in for a text stream.
    """

    # Our own right-button menu
    rmenu_specs = [
        ("Cut", "<<cut>>", "rmenu_check_cut"),
        ("Copy", "<<copy>>", "rmenu_check_copy"),
        ("Paste", "<<paste>>", "rmenu_check_paste"),
    ]

    allow_code_context = False
    allow_highlight_current_line = False

    def __init__(self, *args):
        EditorWindow.__init__(self, *args)

    # Customize EditorWindow
    def ispythonsource(self, filename):
        "Python source is only part of output: do not colorize."
        return False

    def short_title(self):
        "Customize EditorWindow title."
        return "Output"

    def maybesave(self):
        "Customize EditorWindow to not display save file messagebox."
        return 'yes' if self.get_saved() else 'no'

    # Act as output file
    def write(self, s, tags=(), mark="insert"):
        """Write text to text widget.

        The text is inserted at the given index with the provided
        tags.  The text widget is then scrolled to make it visible
        and updated to display it, giving the effect of seeing each
        line as it is added.

        Args:
            s: Text to insert into text widget.
            tags: Tuple of tag strings to apply on the insert.
            mark: Index for the insert.

        Return:
            Length of text inserted.
        """
        assert isinstance(s, str)
        self.text.insert(mark, s, tags)
        self.text.see(mark)
        # Repaint now so output appears line-by-line.  This pumps the Tk event
        # loop re-entrantly, so PyShell overrides write() to skip update() while
        # a subprocess restart is in progress (see PyShell.write_to_console).
        self.text.update()
        return len(s)

    def writelines(self, lines):
        "Write each item in lines iterable."
        for line in lines:
            self.write(line)

    def flush(self):
        "No flushing needed as write() directly writes to widget."
        pass

    def showerror(self, *args, **kwargs):
        messagebox.showerror(*args, **kwargs)


# Currently unused -- kept in case an "open an output window only when something
# is written to it" use case comes back.
class OnDemandOutputWindow:
    "Lazily creates an OutputWindow the first time write() is called."

    tagdefs = {
        # XXX Should use PemPrefs.ColorPrefs
        "stdout":  {"foreground": "blue"},
        "stderr":  {"foreground": "#007700"},
    }

    def __init__(self, flist):
        self.flist = flist
        self.owin = None

    def write(self, s, tags, mark):
        if not self.owin:
            self.setup()
        self.owin.write(s, tags, mark)

    def setup(self):
        self.owin = owin = OutputWindow(self.flist)
        text = owin.text
        for tag, cnf in self.tagdefs.items():
            if cnf:
                text.tag_configure(tag, **cnf)
        text.tag_raise('sel')
        self.write = self.owin.write


if __name__ == '__main__':
    from unittest import main
    main('pem.pem_test.test_outwin', verbosity=2, exit=False)
