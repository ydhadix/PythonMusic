"""PEM's settings system + the Preferences / keybinding dialogs.

Submodules: ``config`` (the pemConf singleton + config-file machinery),
``configdialog`` (the Preferences dialog), ``config_key`` (the keybinding
editor).  ``pemConf`` and ``ConfigChanges`` are re-exported here so existing
``from pem.config import pemConf`` imports keep working now that this
is a package rather than a module.
"""
from pem.config.config import pemConf, ConfigChanges  # noqa: F401
