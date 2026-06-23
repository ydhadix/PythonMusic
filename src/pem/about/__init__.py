"""About Dialog for PEM.

A compact, system-styled window showing the app icon, version, a short
license summary, and a link to the PythonMusic site. It uses ttk widgets so
that it picks up the native appearance of the platform: on macOS it follows
the system light/dark mode automatically (native 'aqua' theme), and on
Windows/Linux it matches the flat IDE look used by the other PEM dialogs.
"""
import os
import re
import sys
import webbrowser

from tkinter import Toplevel, PhotoImage, Text
from tkinter.ttk import Frame, Label, Button, Style

from pem.util import LINK_CURSOR

# Icon shown centered at the top of the dialog.
_ICON_FILE = 'icon_128.png'

# Width of the supporting-text area, in characters. This drives the overall
# window width, since the wrapped text is the widest element.
_BODY_WIDTH_CHARS = 46

# Mid-gray used for the supporting/license text. It deliberately sits between
# the light-mode foreground (near black) and the dark-mode foreground (near
# white) so it reads as a lighter, secondary color in either appearance.
_GRAY = '#808080'

# Link color per appearance: a brighter blue for dark mode, a deeper blue for
# light mode, so the link stays legible against either window background.
_LINK_DARK = '#5aa9ff'
_LINK_LIGHT = '#0a5fcc'

# Flat background used to match the other PEM dialogs on Windows/Linux. On
# macOS we leave the native 'aqua' background in place instead.
_FLAT_BACKGROUND = '#e0e0e0'

# Links written in about.txt. Two forms are recognized: a bare bracketed URL
# like [https://example.com], and a markdown-style [label](https://example.com)
# where 'label' is the friendly text shown in place of the URL.
_LINK_RE = re.compile(
    r'\[([^\]\n]+)\]\((https?://[^)\s]+)\)'   # [label](url)
    r'|\[\s*(https?://[^\]\s]+)\s*\]'          # [url]
)


def _pythonmusic_version():
    try:
        from PythonMusic import __version__ as version
    except Exception:
        version = 'unknown'
    return version


def _license_text():
    here = os.path.abspath(os.path.dirname(__file__))
    try:
        with open(os.path.join(here, 'about.txt'), encoding='utf-8') as f:
            return f.read().strip()
    except OSError:
        return ''


def _iter_about_segments(text):
    """Walk the about text in order, yielding plain-text and link segments.

    Preserving order (rather than pulling links onto their own lines) lets a
    link appear inline, mid-sentence. Each yielded item is a tuple:
    ('text', str) or ('link', label, url).
    """
    text = text.strip()
    position = 0
    for match in _LINK_RE.finditer(text):
        if match.start() > position:
            yield ('text', text[position:match.start()])
        label = match.group(1) or match.group(3)
        url = match.group(2) or match.group(3)
        yield ('link', label, url)
        position = match.end()
    if position < len(text):
        yield ('text', text[position:])


class AboutDialog(Toplevel):
    """Modal 'About PEM' dialog."""

    def __init__(self, parent, *, _htest=False, _utest=False):
        Toplevel.__init__(self, parent)
        self.withdraw()
        self.parent = parent
        self.title('About PEM')
        self.resizable(width=False, height=False)

        self.create_widgets()

        self.protocol("WM_DELETE_WINDOW", self.ok)
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.ok)
        self.button_ok.focus_set()

        if not _utest:
            self.grab_set()
            self._show(_htest)
            self.wait_window()

    def _show(self, htest):
        # The supporting text is a Text widget whose wrapped height can only be
        # measured once it is mapped to its real width. Map the window fully
        # transparent first so we can size the text and center the window
        # without a visible flash, then reveal it.
        faded = self._set_alpha(0.0)
        self.deiconify()
        self._fit_body_height()
        self._center_over_parent(htest)
        if faded:
            self._set_alpha(1.0)

    def _set_alpha(self, value):
        """Set window opacity if the platform supports it; report success."""
        try:
            self.attributes('-alpha', value)
            return True
        except Exception:
            return False

    def _fit_body_height(self):
        self.update_idletasks()
        # count returns the number of display-line boundaries between the two
        # indices, so the final wrapped line needs one more to stay visible.
        line_count = self._body.count('1.0', 'end-1c', 'displaylines')
        if isinstance(line_count, tuple):
            line_count = line_count[0]
        if line_count:
            self._body.configure(height=line_count + 1)
        self.update_idletasks()

    def create_widgets(self):
        # On Windows/Linux, match the flat IDE look used by the other dialogs.
        # On macOS, keep the native 'aqua' appearance so the window follows the
        # system light/dark mode on its own.
        dark = False
        if sys.platform != 'darwin':
            style = Style(self)
            if 'clam' in style.theme_names():
                style.theme_use('clam')
            self.configure(bg=_FLAT_BACKGROUND)
            style.configure('.', background=_FLAT_BACKGROUND)
        else:
            from pem import macosx
            dark = bool(macosx.isDarkMode())

        content = Frame(self, padding=24)
        content.pack(fill='both', expand=True)

        # App icon, centered. Keep a reference so it isn't garbage collected.
        here = os.path.dirname(__file__)
        icon_path = os.path.join(os.path.dirname(here), 'icons', _ICON_FILE)
        if os.path.exists(icon_path):
            self._icon = PhotoImage(master=self, file=icon_path)
            Label(content, image=self._icon).pack(pady=(0, 12))

        # Application name and version. Foreground is left at the ttk default
        # so it adapts to the system appearance on macOS.
        Label(content, text='PEM', font=('TkDefaultFont', 22, 'bold')).pack()
        Label(content, text=f'Version {_pythonmusic_version()}').pack(pady=(0, 12))

        # Supporting text and license summary, with inline clickable links.
        # Its final height is set in _fit_body_height once the window is mapped.
        self._body = self._build_body(content, dark)
        self._body.pack(pady=(0, 12))

        self.button_ok = Button(content, text='Close', command=self.ok)
        self.button_ok.pack()

    def _build_body(self, parent, dark):
        """Build the read-only supporting-text widget with inline links.

        A Text widget (rather than a ttk Label) is used so links can flow
        inline within the prose. Its background is set to the native window
        color so it still follows the system light/dark appearance on macOS.
        """
        background = 'systemWindowBackgroundColor' if sys.platform == 'darwin' \
            else _FLAT_BACKGROUND
        link_color = _LINK_DARK if dark else _LINK_LIGHT

        body = Text(parent, width=_BODY_WIDTH_CHARS, wrap='word',
                    borderwidth=0, highlightthickness=0, padx=0, pady=0,
                    background=background, foreground=_GRAY,
                    cursor='arrow', takefocus=0)
        body.tag_configure('center', justify='center')

        for index, segment in enumerate(_iter_about_segments(_license_text())):
            if segment[0] == 'text':
                body.insert('end', segment[1], 'center')
            else:
                label, url = segment[1], segment[2]
                tag = f'link-{index}'
                body.tag_configure(tag, foreground=link_color, underline=True)
                body.tag_bind(tag, '<Button-1>',
                              lambda event, link=url: webbrowser.open(link))
                body.tag_bind(tag, '<Enter>',
                              lambda event: body.configure(cursor=LINK_CURSOR))
                body.tag_bind(tag, '<Leave>',
                              lambda event: body.configure(cursor='arrow'))
                body.insert('end', label, ('center', tag))

        # Start with a small height; _fit_body_height sets the real value once
        # the widget is mapped. Lock it read-only so it reads as a label.
        body.configure(height=1, state='disabled')
        return body

    def _center_over_parent(self, htest=False):
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()

        parent = self.parent
        if parent is not None and parent.winfo_ismapped():
            parent_x = parent.winfo_rootx()
            parent_y = parent.winfo_rooty()
            parent_w = parent.winfo_width()
            parent_h = parent.winfo_height()
            x = parent_x + (parent_w - width) // 2
            y = parent_y + (parent_h - height) // 2
        else:
            x = (self.winfo_screenwidth() - width) // 2
            y = (self.winfo_screenheight() - height) // 2

        if htest:
            y += 100

        x = max(0, x)
        y = max(0, y)
        self.geometry(f"+{x}+{y}")

    def ok(self, event=None):
        """Dismiss the about dialog."""
        self.grab_release()
        self.destroy()


if __name__ == '__main__':
    # Standalone preview: open the dialog over a small root window.
    from tkinter import Tk
    root = Tk()
    root.title('PEM (preview)')
    root.geometry('500x400')
    AboutDialog(root)
    root.destroy()
