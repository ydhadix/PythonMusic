""" help.py: Implement the Pem help menu.
Contents are subject to revision at any time, without notice.


Help => About PEM: display About Pem dialog

<to be moved here from help_about.py>


Help => PEM Help: Display help.html with proper formatting.
Doc/library/pem.rst (Sphinx)=> Doc/build/html/library/pem.html
(help.copy_strip)=> Lib/pem/help.html

show_pemhelp - Create HelpWindow.  Called in EditorWindow.help_dialog.
"""
import webbrowser

def show_pemhelp(parent):
    "Open the JythonMusic documentation in a web browser."
    webbrowser.open("https://jythonmusic.me/api-reference/")


if __name__ == '__main__':
    from unittest import main
    main('pem.pem_test.test_help', verbosity=2, exit=False)

    from pem.pem_test.htest import run
    run(show_pemhelp)
