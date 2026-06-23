"""Track PEM's top-level windows so the Window menu can list them.

``registry`` (a module-level ``WindowList``) holds every ``ListedToplevel``.
The Window menu is rebuilt from it on demand, and registered callbacks fire
whenever a window is added or removed -- which is also how PEM knows to quit
the Tk main loop once the last window closes.
"""
from tkinter import Toplevel, TclError
import sys


class WindowList:
    "Registry of open top-level windows; fires callbacks on add/remove."

    def __init__(self):
        self.dict = {}
        self.callbacks = []

    def add(self, window):
        window.after_idle(self.call_callbacks)
        self.dict[str(window)] = window

    def delete(self, window):
        try:
            del self.dict[str(window)]
        except KeyError:
            # Sometimes, destroy() is called twice
            pass
        self.call_callbacks()

    def add_windows_to_menu(self,  menu):
        list = []
        for key in self.dict:
            window = self.dict[key]
            try:
                title = window.get_title()
            except TclError:
                continue
            list.append((title, key, window))
        list.sort()
        for title, key, window in list:
            menu.add_command(label=title, command=window.wakeup)

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def unregister_callback(self, callback):
        try:
            self.callbacks.remove(callback)
        except ValueError:
            pass

    def call_callbacks(self):
        for callback in self.callbacks:
            try:
                callback()
            except:
                t, v, tb = sys.exc_info()
                print("warning: callback failed in WindowList", t, ":", v)


registry = WindowList()

add_windows_to_menu = registry.add_windows_to_menu
register_callback = registry.register_callback
unregister_callback = registry.unregister_callback


class ListedToplevel(Toplevel):
    "A Toplevel that registers itself with the module ``registry`` so it shows in the Window menu."

    def __init__(self, master, **kw):
        Toplevel.__init__(self, master, kw)
        registry.add(self)
        self.focused_widget = self

    def destroy(self):
        registry.delete(self)
        Toplevel.destroy(self)
        # If this is Pem's last window then quit the mainloop
        # (Needed for clean exit on Windows 98)
        if not registry.dict:
            self.quit()

    def update_windowlist_registry(self, window):
        registry.call_callbacks()

    def get_title(self):
        # Subclass can override
        return self.wm_title()

    def wakeup(self):
        try:
            if self.wm_state() == "iconic":
                self.wm_withdraw()
                self.wm_deiconify()
            self.tkraise()
            self.focused_widget.focus_set()
        except TclError:
            # This can happen when the Window menu was torn off.
            # Simply ignore it.
            pass


if __name__ == "__main__":
    from unittest import main
    main('pem.pem_test.test_window', verbosity=2)
