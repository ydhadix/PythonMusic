"""File open/save for an editor window: dialogs, encoding handling, autosave.

``IOBinding`` (one per editor window) backs <<open-window-from-file>>,
<<save-window>>, etc. -- reading a file with the right encoding, writing it back,
prompting on unsaved changes, and tracking the window's filename/dirname.  It
also re-exports ``encoding`` / ``errors`` from ``pem._encoding`` for
backward compatibility (the subprocess imports those without touching tkinter).
"""
import io
import os
import shlex
import sys
import tempfile
import tokenize

from tkinter import filedialog
from tkinter import messagebox
from tkinter.simpledialog import askstring  # loadfile encoding.

from pem.config import pemConf
from pem.util import py_extensions
from pem._encoding import encoding, errors  # noqa: F401  (re-exported)

py_extensions = ' '.join("*"+ext for ext in py_extensions)


# Globally-tracked directory for file open/save dialogs.  Persisted via
# pemConf so it survives PEM (and frozen-PEM) restarts.  Every IOBinding
# dialog (open, save, save-as, save-a-copy) reads and updates this on each
# invocation so the dialog default is consistent across editors and shells.
_DIALOG_DIR_SECTION = 'General'
_DIALOG_DIR_OPTION  = 'last-dialog-dir'

def _get_dialog_dir(fallback):
    "Return the persisted dialog directory, or 'fallback' if unset/missing."
    persisted = pemConf.GetOption('main', _DIALOG_DIR_SECTION, _DIALOG_DIR_OPTION,
                                  default='', warn_on_default=False)
    if persisted and os.path.isdir(persisted):
        return persisted
    return fallback

def _set_dialog_dir(path):
    "Record the directory containing 'path' as the global dialog directory."
    if not path:
        return
    directory = os.path.dirname(os.path.abspath(path))
    if directory and os.path.isdir(directory):
        pemConf.SetOption('main', _DIALOG_DIR_SECTION, _DIALOG_DIR_OPTION, directory)
        pemConf.userCfg['main'].Save()   # flush so a crash doesn't lose it


class IOBinding:
    "File I/O (open/save/encoding/autosave) for one editor window."
    # One instance per editor Window so methods know which to save, close.
    # Open returns focus to self.editwin if aborted.
    # EditorWindow.open_module, others, belong here.

    def __init__(self, editwin):
        self.editwin = editwin
        self.text = editwin.text
        self.__id_open = self.text.bind("<<open-window-from-file>>", self.open)
        self.__id_save = self.text.bind("<<save-window>>", self.save)
        self.__id_saveas = self.text.bind("<<save-window-as-file>>",
                                          self.save_as)
        self.__id_savecopy = self.text.bind("<<save-copy-of-window-as-file>>",
                                            self.save_a_copy)
        self.fileencoding = 'utf-8'
        self.__id_print = self.text.bind("<<print-window>>", self.print_window)
        # External-change tracking: stat-based signature of self.filename at
        # last successful load/save.  Compared on focus-in and at save time
        # so changes made outside PEM aren't silently lost.
        self._fs_mtime = None
        self._fs_size  = None
        self._check_in_progress = False
        self.__id_focusin = self.text.bind("<FocusIn>",
                                           self._on_focus_in, add="+")

    def close(self):
        # Undo command bindings
        self.text.unbind("<<open-window-from-file>>", self.__id_open)
        self.text.unbind("<<save-window>>", self.__id_save)
        self.text.unbind("<<save-window-as-file>>",self.__id_saveas)
        self.text.unbind("<<save-copy-of-window-as-file>>", self.__id_savecopy)
        self.text.unbind("<<print-window>>", self.__id_print)
        self.text.unbind("<FocusIn>", self.__id_focusin)
        # Break cycles
        self.editwin = None
        self.text = None
        self.filename_change_hook = None

    def get_saved(self):
        return self.editwin.get_saved()

    def set_saved(self, flag):
        self.editwin.set_saved(flag)

    def reset_undo(self):
        self.editwin.reset_undo()

    filename_change_hook = None

    def set_filename_change_hook(self, hook):
        self.filename_change_hook = hook

    filename = None
    dirname = None

    def set_filename(self, filename):
        if filename and os.path.isdir(filename):
            self.filename = None
            self.dirname = filename
        else:
            self.filename = filename
            self.dirname = None
            self.set_saved(1)
            if self.filename_change_hook:
                self.filename_change_hook()

    def open(self, event=None, editFile=None):
        flist = self.editwin.flist
        # Save in case parent window is closed (ie, during askopenfile()).
        if flist:
            if not editFile:
                filename = self.askopenfile()
            else:
                filename=editFile
            if filename:
                # If editFile is valid and already open, flist.open will
                # shift focus to its existing window.
                # If the current window exists and is a fresh unnamed,
                # unmodified editor window (not an interpreter shell),
                # pass self.loadfile to flist.open so it will load the file
                # in the current window (if the file is not already open)
                # instead of a new window.
                if (self.editwin and
                        not getattr(self.editwin, 'interp', None) and
                        not self.filename and
                        self.get_saved() and
                        not getattr(self.editwin, '_user_created', False)):
                    flist.open(filename, self.loadfile)
                else:
                    flist.open(filename)
            else:
                if self.text:
                    self.text.focus_set()
            return "break"

        # Code for use outside PEM:
        if self.get_saved():
            reply = self.maybesave()
            if reply == "cancel":
                self.text.focus_set()
                return "break"
        if not editFile:
            filename = self.askopenfile()
        else:
            filename=editFile
        if filename:
            self.loadfile(filename)
        else:
            self.text.focus_set()
        return "break"

    eol_convention = os.linesep  # default

    # ── External-change detection ────────────────────────────────────────────
    #
    # We stat self.filename after every successful load/save and keep the
    # (mtime, size) signature.  _disk_state() compares the current disk state
    # to that signature to detect external modifications.

    def _capture_fs_signature(self, filename):
        "Record the (mtime, size) of filename as the last-known signature."
        try:
            stat = os.stat(filename)
            self._fs_mtime = stat.st_mtime
            self._fs_size  = stat.st_size
        except OSError:
            self._fs_mtime = None
            self._fs_size  = None

    def _disk_state(self):
        """Return one of:
          'unknown'   — no filename, or never loaded/saved (no signature)
          'unchanged' — disk matches our last-known signature
          'changed'   — disk file exists but signature differs
          'missing'   — file no longer exists on disk
        """
        if not self.filename or self._fs_mtime is None:
            return 'unknown'
        try:
            stat = os.stat(self.filename)
        except OSError:
            return 'missing'
        if stat.st_mtime == self._fs_mtime and stat.st_size == self._fs_size:
            return 'unchanged'
        return 'changed'

    def _on_focus_in(self, event=None):
        "Editor text widget became focused — check for external changes."
        if self._check_in_progress:
            return
        state = self._disk_state()
        if state in ('unknown', 'unchanged'):
            return
        self._check_in_progress = True
        try:
            if state == 'missing':
                # File deleted out from under us; next save will recreate it.
                self.set_saved(False)
            elif self.get_saved():
                # Clean buffer — silent reload.
                self._reload_preserving_cursor()
            else:
                # Dirty buffer — must prompt.
                if self._prompt_focusin_dirty():
                    self.loadfile(self.filename)
                else:
                    # User chose Keep buffer; treat this acknowledgement as
                    # accepting the current disk state so we don't re-prompt
                    # on every focus-in until the file changes again.
                    self._capture_fs_signature(self.filename)
        finally:
            self._check_in_progress = False

    def _reload_preserving_cursor(self):
        "Reload self.filename, keeping the cursor on the same line if possible."
        try:
            cursor_line = int(self.text.index("insert").split('.')[0])
        except Exception:
            cursor_line = 1
        if not self.loadfile(self.filename):
            return
        try:
            last_line = int(self.text.index("end-1c").split('.')[0])
            target = max(1, min(cursor_line, last_line))
            self.text.mark_set("insert", f"{target}.0")
            self.text.see("insert")
        except Exception:
            pass

    def _prompt_focusin_dirty(self):
        """Buffer is dirty and the file has changed externally.
        Returns True if the user wants to reload, False to keep the buffer.
        """
        return bool(messagebox.askyesno(
            title="File changed on disk",
            message=(f"'{self.filename}' was updated by another program.\n\n"
                     "Discard your changes and load the updated file?"),
            default=messagebox.YES,
            parent=self.text,
        ))

    def _prompt_save_conflict(self):
        """User triggered a save but the file has changed externally.
        Returns True to overwrite, False to abandon the save.
        """
        return bool(messagebox.askyesno(
            title="File changed on disk",
            message=(f"'{self.filename}' was updated by another program.\n\n"
                     "Save anyway?"),
            default=messagebox.YES,
            parent=self.text,
        ))

    def _prompt_close_save_conflict(self):
        """User triggered close-with-save but the file has changed externally.
        Returns 'overwrite' (save and close), 'discard' (close without saving),
        or 'cancel' (stay open).
        """
        choice = messagebox.askyesnocancel(
            title="File changed on disk",
            message=(f"'{self.filename}' was updated by another program.\n\n"
                     "Save anyway?"),
            default=messagebox.YES,
            parent=self.text,
        )
        if choice is None:
            return 'cancel'
        return 'overwrite' if choice else 'discard'

    def loadfile(self, filename):
        try:
            try:
                with tokenize.open(filename) as f:
                    chars = f.read()
                    fileencoding = f.encoding
                    eol_convention = f.newlines
                    converted = False
            except (UnicodeDecodeError, SyntaxError):
                # Wait for the editor window to appear
                self.editwin.text.update()
                enc = askstring(
                    "Specify file encoding",
                    "The file's encoding is invalid for Python 3.x.\n"
                    "PEM will convert it to UTF-8.\n"
                    "What is the current encoding of the file?",
                    initialvalue='utf-8',
                    parent=self.editwin.text)
                with open(filename, encoding=enc) as f:
                    chars = f.read()
                    fileencoding = f.encoding
                    eol_convention = f.newlines
                    converted = True
        except OSError as err:
            messagebox.showerror("I/O Error", str(err), parent=self.text)
            return False
        except UnicodeDecodeError:
            messagebox.showerror("Decoding Error",
                                   "File %s\nFailed to Decode" % filename,
                                   parent=self.text)
            return False

        if not isinstance(eol_convention, str):
            # If the file does not contain line separators, it is None.
            # If the file contains mixed line separators, it is a tuple.
            if eol_convention is not None:
                messagebox.showwarning("Mixed Newlines",
                                         "Mixed newlines detected.\n"
                                         "The file will be changed on save.",
                                         parent=self.text)
                converted = True
            eol_convention = os.linesep  # default

        self.text.delete("1.0", "end")
        self.set_filename(None)
        self.fileencoding = fileencoding
        self.eol_convention = eol_convention
        self.text.insert("1.0", chars)
        self.reset_undo()
        self.set_filename(filename)
        if converted:
            # We need to save the conversion results first
            # before being able to execute the code
            self.set_saved(False)
        self.text.mark_set("insert", "1.0")
        self.text.yview("insert")
        self.updaterecentfileslist(filename)
        self._capture_fs_signature(filename)
        return True

    def maybesave(self):
        """Return 'yes', 'no', 'cancel' as appropriate.

        Tkinter messagebox.askyesnocancel converts these tk responses
        to True, False, None.  Convert back, as now expected elsewhere.
        """
        if self.get_saved():
            return "yes"
        message = ("Do you want to save "
                   f"{self.filename or 'this untitled document'}"
                   " before closing?")
        confirm = messagebox.askyesnocancel(
                  title="Save On Close",
                  message=message,
                  default=messagebox.YES,
                  parent=self.text)
        if confirm is None:
            reply = "cancel"
        elif not confirm:
            reply = "no"
        elif not self.filename:
            # Untitled — let save_as handle filename selection.
            self.save_as(None)
            reply = "yes" if self.get_saved() else "cancel"
        elif self._disk_state() == 'changed':
            # External change while close+save is in flight — different
            # options than the standalone save flow ("close without saving"
            # instead of "reload first").
            choice = self._prompt_close_save_conflict()
            if choice == 'overwrite':
                if self.writefile(self.filename):
                    self.set_saved(True)
                reply = "yes" if self.get_saved() else "cancel"
            elif choice == 'discard':
                reply = "no"
            else:
                reply = "cancel"
        else:
            if self.writefile(self.filename):
                self.set_saved(True)
            reply = "yes" if self.get_saved() else "cancel"
        self.text.focus_set()
        return reply

    def save(self, event):
        if not self.filename:
            self.save_as(event)
        elif self._disk_state() == 'changed' and not self._prompt_save_conflict():
            pass   # user declined to overwrite — return to editor
        else:
            if self.writefile(self.filename):
                self.set_saved(True)
        self.text.focus_set()
        return "break"

    def save_as(self, event):
        filename = self.asksavefile()
        if filename:
            if self.writefile(filename):
                self.set_filename(filename)
                self.set_saved(1)
                # set_filename made `filename` our new backing file;
                # capture its signature now that the association is in place.
                self._capture_fs_signature(filename)
        self.text.focus_set()
        self.updaterecentfileslist(filename)
        return "break"

    def save_a_copy(self, event):
        filename = self.asksavefile()
        if filename:
            self.writefile(filename)
        self.text.focus_set()
        self.updaterecentfileslist(filename)
        return "break"

    def writefile(self, filename):
        text = self.fixnewlines()
        chars = self.encode(text)
        try:
            with open(filename, "wb") as f:
                f.write(chars)
                f.flush()
                os.fsync(f.fileno())
            # Refresh the signature when we wrote our own backing file;
            # save_a_copy targets a different path and must not affect it.
            if filename == self.filename:
                self._capture_fs_signature(filename)
            return True
        except OSError as msg:
            messagebox.showerror("I/O Error", str(msg),
                                   parent=self.text)
            return False

    def fixnewlines(self):
        """Return text with os eols.

        Add prompts if shell else final \n if missing.
        """

        if hasattr(self.editwin, "interp"):  # Saving shell.
            text = self.editwin.get_prompt_text('1.0', self.text.index('end-1c'))
        else:
            if self.text.get("end-2c") != '\n':
                self.text.insert("end-1c", "\n")  # Changes 'end-1c' value.
            text = self.text.get('1.0', "end-1c")
        if self.eol_convention != "\n":
            text = text.replace("\n", self.eol_convention)
        return text

    def encode(self, chars):
        if isinstance(chars, bytes):
            # This is either plain ASCII, or Tk was returning mixed-encoding
            # text to us. Don't try to guess further.
            return chars
        # Preserve a BOM that might have been present on opening
        if self.fileencoding == 'utf-8-sig':
            return chars.encode('utf-8-sig')
        # See whether there is anything non-ASCII in it.
        # If not, no need to figure out the encoding.
        try:
            return chars.encode('ascii')
        except UnicodeEncodeError:
            pass
        # Check if there is an encoding declared
        try:
            encoded = chars.encode('ascii', 'replace')
            enc, _ = tokenize.detect_encoding(io.BytesIO(encoded).readline)
            return chars.encode(enc)
        except SyntaxError as err:
            failed = str(err)
        except UnicodeEncodeError:
            failed = "Invalid encoding '%s'" % enc
        messagebox.showerror(
            "I/O Error",
            "%s.\nSaving as UTF-8" % failed,
            parent=self.text)
        # Fallback: save as UTF-8, with BOM - ignoring the incorrect
        # declared encoding
        return chars.encode('utf-8-sig')

    def print_window(self, event):
        confirm = messagebox.askokcancel(
                  title="Print",
                  message="Print to Default Printer",
                  default=messagebox.OK,
                  parent=self.text)
        if not confirm:
            self.text.focus_set()
            return "break"

        # Always build a numbered temp file for printing — even if the
        # tab is saved on disk, we want line-numbered output rather than
        # the raw source file.
        saved = self.get_saved()
        if saved:
            source_filename = self.filename
        else:
            source_filename = None

        # Get the current text content (from disk if saved, from the
        # editor if not).
        if source_filename:
            try:
                with open(source_filename, encoding='utf-8',
                          errors='replace') as src:
                    content = src.read()
            except OSError:
                content = self.text.get('1.0', 'end-1c')
        else:
            content = self.text.get('1.0', 'end-1c')

        # Number every line. Width auto-sizes to total line count so the
        # numbers align cleanly.
        lines = content.splitlines()
        width = max(len(str(len(lines))), 3)
        numbered = '\n'.join(f"{i+1:>{width}}  {line}"
                            for i, line in enumerate(lines))
        if not numbered.endswith('\n'):
            numbered += '\n'

        # Write the numbered version to a temp file and print that.
        (tfd, tempfilename) = tempfile.mkstemp(prefix='PEM_tmp_',
                                               suffix='.txt')
        filename = tempfilename
        try:
            with os.fdopen(tfd, 'w', encoding='utf-8') as f:
                f.write(numbered)
        except OSError as msg:
            messagebox.showerror("I/O Error", str(msg), parent=self.text)
            os.unlink(tempfilename)
            return "break"

        platform = os.name
        printPlatform = True
        if platform == 'posix': #posix platform
            command = pemConf.GetOption('main','General',
                                         'print-command-posix')
            command = command + " 2>&1"
        elif platform == 'nt': #win32 platform
            command = pemConf.GetOption('main','General','print-command-win')
        else: #no printing for this platform
            printPlatform = False
        if printPlatform:  #we can try to print for this platform
            command = command % shlex.quote(filename)
            pipe = os.popen(command, "r")
            # things can get ugly on NT if there is no printer available.
            output = pipe.read().strip()
            status = pipe.close()
            if status:
                output = "Printing failed (exit status 0x%x)\n" % \
                         status + output
            if output:
                output = "Printing command: %s\n" % repr(command) + output
                messagebox.showerror("Print status", output, parent=self.text)
        else:  #no printing for this platform
            message = "Printing is not enabled for this platform: %s" % platform
            messagebox.showinfo("Print status", message, parent=self.text)
        if tempfilename:
            os.unlink(tempfilename)
        return "break"

    opendialog = None
    savedialog = None

    filetypes = (
        ("Python files", py_extensions, "TEXT"),
        ("Text files", "*.txt", "TEXT"),
        ("All files", "*"),
        )

    defaultextension = '.py' if sys.platform == 'darwin' else ''


    def defaultfilename(self, mode="open"):
            if self.filename:
                return os.path.split(self.filename)
            elif self.dirname:
                return self.dirname, ""
            else:
                try:
                    pwd = os.getcwd()
                except OSError:
                    pwd = ""
                return pwd, ""


    def askopenfile(self):
        dir, base = self.defaultfilename("open")
        dir = _get_dialog_dir(dir)
        opendialog = filedialog.Open(parent=self.text, filetypes=self.filetypes)
        filename = opendialog.show(initialdir=dir, initialfile=base)
        if filename:
            _set_dialog_dir(filename)
        return filename


    def asksavefile(self):
        dir, base = self.defaultfilename("save")
        # For a never-saved document there is no backing filename, so pre-fill the
        # dialog with the editor tab's name ("untitled X") instead of leaving it blank.
        if not base and hasattr(self.editwin, "short_title"):
            base = self.editwin.short_title()
        dir = _get_dialog_dir(dir)
        # On macOS, giving the save panel a parent window shows it as a sheet whose
        # filename field does not take visible focus (no caret or selection) until it is
        # clicked.  Opening it without a parent shows it as an app-modal panel with the
        # prefilled name focused and selected as expected.  Other platforms keep the
        # parent for correct modality and window placement.  (self.text is still passed
        # as the master so the dialog has a Tcl context either way.)
        savedialog_options = {
                'filetypes': self.filetypes,
                'defaultextension': self.defaultextension}
        if self.text.tk.call('tk', 'windowingsystem') != 'aqua':
            savedialog_options['parent'] = self.text
        savedialog = filedialog.SaveAs(self.text, **savedialog_options)
        filename = savedialog.show(initialdir=dir, initialfile=base)
        if filename:
            _set_dialog_dir(filename)
        return filename


    def updaterecentfileslist(self, filename):
            "Update recent file list on all editor windows"
            if self.editwin.flist:
                self.editwin.update_recent_files_list(filename)


def _io_binding(parent):  # htest #
    from tkinter import Toplevel, Text

    top = Toplevel(parent)
    top.title("Test IOBinding")
    x, y = map(int, parent.geometry().split('+')[1:])
    top.geometry("+%d+%d" % (x, y + 175))

    class MyEditWin:
        def __init__(self, text):
            self.text = text
            self.flist = None
            self.text.bind("<Control-o>", self.open)
            self.text.bind('<Control-p>', self.print)
            self.text.bind("<Control-s>", self.save)
            self.text.bind("<Alt-s>", self.saveas)
            self.text.bind('<Control-c>', self.savecopy)
        def get_saved(self): return 0
        def set_saved(self, flag): pass
        def reset_undo(self): pass
        def open(self, event):
            self.text.event_generate("<<open-window-from-file>>")
        def print(self, event):
            self.text.event_generate("<<print-window>>")
        def save(self, event):
            self.text.event_generate("<<save-window>>")
        def saveas(self, event):
            self.text.event_generate("<<save-window-as-file>>")
        def savecopy(self, event):
            self.text.event_generate("<<save-copy-of-window-as-file>>")

    text = Text(top)
    text.pack()
    text.focus_set()
    editwin = MyEditWin(text)
    IOBinding(editwin)


if __name__ == "__main__":
    from unittest import main
    main('pem.pem_test.test_iomenu', verbosity=2, exit=False)

    from pem.pem_test.htest import run
    run(_io_binding)
