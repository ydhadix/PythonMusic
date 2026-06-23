#!/usr/bin/env python3
"""Build an outline/ skeleton (folders + section index.md files) from a mkdocs nav.

Reads a mkdocs.yml (given as an argument, or prompted for), walks its `nav:`, and
creates a folder + index.md for:

  * every *section* (a nav entry with children) — its index.md uses the section's
    title as its H1, a description placeholder, and a table linking to that level's
    contents; and
  * every *leaf directory page* (a nav entry whose target is a `…/index.md`, e.g. a
    class like Rectangle or a single-page library) — its index.md gets the title and
    a description placeholder, but no table (its own contents, such as a method
    table, are filled in by other tools).

Leaf entries that point at a regular page file (e.g. `display.md`, `constants.md`)
are linked from their parent's table but not generated. Output goes to ./_outline/
(relative to the current working directory), cleared first.

    python build_outline.py ../../mkdocs.yml      # e.g. run from _scripts/
    python build_outline.py                       # prompts for the path
"""

import posixpath
import shutil
import sys
from pathlib import Path

import yaml


PLACEHOLDER = "<!-- Description -->"
VISIBLE_PLACEHOLDER = "[Description]"

INDEX_PAGE = """\
# {title}

{placeholder}

{table}"""

TABLE = """
| Contents | <!-- Description --> |
|---|---|
{rows}

"""

ROW = "| [{title}]({link}) | {placeholder} |"


# Tolerate any custom YAML tags (e.g. !ENV, !!python/name:...) so we can read
# any mkdocs.yml without needing the plugins that define them.
class _Loader(yaml.SafeLoader):
    pass


_Loader.add_multi_constructor("", lambda loader, suffix, node: None)


def parse_item(item):
    """(title, value) for a nav entry; value is a str (page file) or list (children)."""
    if isinstance(item, dict):
        return next(iter(item.items()))
    if isinstance(item, str):
        return None, item
    return None, None


def is_section(value):
    return isinstance(value, list)


def is_dir_page(value):
    """A leaf nav target that is a directory index page (`…/index.md`)."""
    return isinstance(value, str) and posixpath.basename(value) == "index.md"


def find_index(children):
    """The index.md file listed directly under a section, if any."""
    for child in children:
        _, value = parse_item(child)
        if isinstance(value, str) and posixpath.basename(value) == "index.md":
            return value
    return None


def collect_files(children):
    files = []
    for child in children:
        _, value = parse_item(child)
        if isinstance(value, str):
            files.append(value)
        elif is_section(value):
            files.extend(collect_files(value))
    return files


def section_dir(children):
    """Directory a section maps to: its index.md's folder, else the common folder
    of its descendant files."""
    index = find_index(children)
    if index:
        return posixpath.dirname(index)
    dirs = [posixpath.dirname(f) for f in collect_files(children)] or [""]
    return posixpath.commonpath(dirs) if len(dirs) > 1 else dirs[0]


def child_target(value):
    """File a table row links to: a page's file, or a subsection's index.md."""
    if is_section(value):
        return posixpath.join(section_dir(value), "index.md")
    return value


def build_rows(children, here, own_index):
    rows = []
    for child in children:
        title, value = parse_item(child)
        target = child_target(value)
        if target == own_index:                 # skip the section's own index entry
            continue
        if title is None:                        # bare page -> title from filename
            title = posixpath.splitext(posixpath.basename(value))[0]
        link = posixpath.relpath(target, here)
        rows.append(ROW.format(title=title, link=link, placeholder=PLACEHOLDER))
    return rows


def process_section(out_root, title, children, counter):
    here = section_dir(children)
    own_index = find_index(children)

    folder = out_root / here
    folder.mkdir(parents=True, exist_ok=True)

    rows = build_rows(children, here, own_index)
    table = TABLE.format(rows="\n".join(rows)) if rows else ""
    page = INDEX_PAGE.format(title=title, placeholder=VISIBLE_PLACEHOLDER, table=table)
    (folder / "index.md").write_text(page.rstrip() + "\n", encoding="utf-8")
    counter[0] += 1

    for child in children:
        child_title, child_value = parse_item(child)
        if is_section(child_value):
            process_section(out_root, child_title, child_value, counter)
        elif is_dir_page(child_value) and child_value != own_index:
            process_page(out_root, child_title, child_value, counter)


def process_page(out_root, title, value, counter):
    """Create a folder + skeleton index.md for a leaf directory page (a class or
    single-page library whose nav target is `…/index.md`). No table is written —
    its own contents (e.g. a method table) are filled in by other tools."""
    folder = out_root / posixpath.dirname(value)
    folder.mkdir(parents=True, exist_ok=True)
    page = INDEX_PAGE.format(title=title, placeholder=VISIBLE_PLACEHOLDER, table="")
    (folder / "index.md").write_text(page.rstrip() + "\n", encoding="utf-8")
    counter[0] += 1


def main():
    raw = sys.argv[1] if len(sys.argv) > 1 else input("Path to mkdocs.yml: ").strip()
    config_path = Path(raw).expanduser()
    if not config_path.is_file():
        print(f"error: not a file: {config_path}", file=sys.stderr)
        sys.exit(1)

    config = yaml.load(config_path.read_text(encoding="utf-8"), Loader=_Loader) or {}
    nav = config.get("nav")
    if not nav:
        print("error: no 'nav' found in the config", file=sys.stderr)
        sys.exit(1)

    out_root = Path("_outline")
    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True)

    counter = [0]
    for item in nav:
        title, value = parse_item(item)
        if is_section(value):
            process_section(out_root, title, value, counter)
        elif is_dir_page(value):
            process_page(out_root, title, value, counter)

    print(f"Created {counter[0]} index file(s) under {out_root}/")


if __name__ == "__main__":
    main()
