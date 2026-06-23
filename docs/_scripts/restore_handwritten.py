#!/usr/bin/env python3
"""Copy nav-referenced, hand-authored pages from the live docs into a staged tree.

The page generators (build_outline, style_api) own section overviews and the
class/method/function pages, but a few pages the nav points at are authored by hand
and produced by no script — chiefly the constant tables (the music constants and the
MIDI event constants). When the whole API tree is rebuilt into a staging directory,
those pages are absent from it.

This copies across every page the nav references that exists in the live tree but not
the staged one, so the staged tree is complete and ready to promote. Pages left over
in the live tree from an earlier nav (orphans no longer referenced) are not copied, so
a layout change drops them cleanly.

    python restore_handwritten.py <mkdocs.yml> <live_root> <staged_root>

<live_root> and <staged_root> are the doc roots the nav's targets are relative to
(e.g. `docs` and `docs/_scripts/_outline`).
"""

import shutil
import sys
from pathlib import Path

import yaml


class _Loader(yaml.SafeLoader):
    """Tolerate custom mkdocs tags (e.g. !ENV) so any config loads."""


_Loader.add_multi_constructor("", lambda loader, suffix, node: None)


def nav_targets(nav, out=None):
    """Every `.md` file the nav points at (sections recursed into)."""
    if out is None:
        out = []
    for item in nav:
        value = next(iter(item.values())) if isinstance(item, dict) else item
        if isinstance(value, list):
            nav_targets(value, out)
        elif isinstance(value, str) and value.endswith(".md"):
            out.append(value)
    return out


def main():
    if len(sys.argv) != 4:
        print("usage: python restore_handwritten.py <mkdocs.yml> <live_root> <staged_root>",
              file=sys.stderr)
        sys.exit(1)

    config_path, live_raw, staged_raw = sys.argv[1:4]
    config = yaml.load(Path(config_path).read_text(encoding="utf-8"), Loader=_Loader) or {}
    live_root = Path(live_raw).expanduser()
    staged_root = Path(staged_raw).expanduser()

    copied = 0
    for target in nav_targets(config.get("nav") or []):
        source = live_root / target
        destination = staged_root / target
        if source.exists() and not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            copied += 1
            print(f"  restored {target}")

    print(f"Restored {copied} hand-authored page(s) from {live_root} into {staged_root}")


if __name__ == "__main__":
    main()
