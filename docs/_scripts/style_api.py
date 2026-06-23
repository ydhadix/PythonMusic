#!/usr/bin/env python3
"""Generate API reference pages from the JSON produced by extract_api.py.

Two modes:

  methods+classes   (re)generate every class's index.md AND its per-method pages
  methods           (re)generate only the per-method pages (class index.md files,
                    which are hand-maintained after the initial run, are left alone)

A class is placed using the mkdocs nav: it maps to the leaf nav entry *titled with
the class name* whose target is a `…/<class>/index.md`. (Matching by title rather
than directory avoids colliding with sections such as "Graphics"/"Control" whose
folders share a class's lowercased name.)

Inheritance is resolved by walking each class's single-base chain to the root;
a subclass member overrides an inherited one of the same name, and inherited
members are written into the subclass's own directory using the subclass's
instance name. Classes found in the JSON but absent from the nav, and any base
classes that can't be resolved, are reported at the end.

Free (module-level) functions are placed by the nav, not by their module:

  * Any leaf entry whose target is `<dir>/<name>.md` (not `index.md` or
    `constants.md`) is a *per-function page*. If `<name>` matches a module
    function, that function's page is generated there. This lets a class-bearing
    module advertise selected functions (e.g. music's noteToFreq/freqToNote) while
    omitting others (mapScale), purely by what the nav lists.
  * A *function library* — a module with no classes (e.g. utilities, zipf) — also
    gets an index page. When the nav advertises its functions individually (a
    "section" of per-function pages, like Mapping Values), the index lists exactly
    those, in nav order, and only those pages are generated. When the nav lists
    only the library's Overview (no per-function entries, like Zipf), every public
    function is generated and listed instead.

A nav `.md` leaf that matches no function (e.g. a class mistakenly given a flat
page instead of a `<class>/index.md` directory) is reported at the end.

    python style_api.py <mkdocs.yml> <json_dir> <target_dir> <mode>

If <target_dir> doesn't yet contain the folders, they are created.
"""

import json
import posixpath
import re
import sys
from pathlib import Path

import yaml


MODES = {"methods+classes", "classes+methods", "methods"}

NO_DOCSTRING = "_No Docstring_"
SECTION_DESC = "[Description]"          # visible placeholder for hand-authored prose
ROW_DESC = "<!-- Description -->"       # invisible per-row placeholder

# Annotation text swaps for the API guide, applied (in order) to each type before
# it is written into an argument table. The guide reads as prose, so we prefer plain
# words over literal typing syntax. Add a literal->replacement pair here to extend.
# NOTE: annotations carry spaces around the union pipe (e.g. "int | float"), so the
#       bare "|" -> "or" swap yields "int or float"; it also keeps the pipe out of
#       the markdown cell, where it would otherwise read as a column separator.
ANNOTATION_DISPLAY = {
    "Callable": "function",
    "|": "or",
}

# Order the `### <group>` blocks of functions appear in on a class page. Groups are
# declared per method in the source with `# doc-group:` markers (see extract_api.py);
# this fixes only their *order*, not their membership. A class's methods that carry no
# group sit in the headerless table above these blocks; a group seen in the source but
# absent here is appended after the known ones, in first-seen order.
DOC_GROUP_ORDER = [
    "Position", "Size", "Rotation", "Visibility", "Color",
    "Information", "Hit Testing", "Events", "Grouping",
]


# --- mkdocs.yml --------------------------------------------------------------

class _Loader(yaml.SafeLoader):
    """Tolerate custom mkdocs tags (e.g. !ENV) so any config loads."""


_Loader.add_multi_constructor("", lambda loader, suffix, node: None)


def parse_item(item):
    if isinstance(item, dict):
        return next(iter(item.items()))
    if isinstance(item, str):
        return None, item
    return None, None


def first_index_dir(children):
    """Directory of a section's own index.md (its first `…/index.md` child)."""
    for child in children:
        _, value = parse_item(child)
        if isinstance(value, str) and posixpath.basename(value) == "index.md":
            return posixpath.dirname(value)
    return None


def walk_nav(nav, section_dirs, leaf_pages):
    """Gather a section's own-index directories and every leaf `…/index.md` page.

    section_dirs: directories that hold a *section's* own index (an "Overview").
    leaf_pages:   (title, directory) for every leaf entry targeting `…/index.md`.
    """
    for item in nav:
        title, value = parse_item(item)
        if isinstance(value, list):
            own = first_index_dir(value)
            if own is not None:
                section_dirs.add(own)
            walk_nav(value, section_dirs, leaf_pages)
        elif isinstance(value, str) and posixpath.basename(value) == "index.md":
            leaf_pages.append((title, posixpath.dirname(value)))
    return section_dirs, leaf_pages


def class_dir_lookup(nav):
    """Build name/basename -> directory maps (and dir -> title) for leaf pages.

    A page counts as a leaf (class or single-page library) only if its directory
    is *not* a section's own index location (so section overviews like
    `api/gui/graphics/index.md` are excluded, but a standalone leaf like
    `api/automate/index.md` is included). Classes are matched first by nav title,
    then by directory basename (the class name lowercased) — the latter covers
    entries whose nav label differs from the class name (e.g. "Automation Library"
    -> `automate/` -> Automate). Free-function libraries are matched by directory
    basename against their module stem (e.g. `utilities.py` -> `utilities/`), so
    their nav label is free to differ (e.g. "Value Shaping"); `by_directory_title`
    supplies that label as the generated page's heading.
    """
    section_dirs, leaf_pages = walk_nav(nav, set(), [])
    by_title, by_basename, by_directory_title = {}, {}, {}
    for title, directory in leaf_pages:
        if directory in section_dirs:
            continue
        if title is not None:
            by_title[title] = directory
            by_directory_title[directory] = title
        by_basename[posixpath.basename(directory)] = directory
    return by_title, by_basename, by_directory_title


def locate_class(name, by_title, by_basename):
    if name in by_title:
        return by_title[name]
    return by_basename.get(name.lower())


def function_leaf_pages(nav, out=None):
    """(name, directory) for every leaf targeting `<dir>/<name>.md` — a per-function
    page. `index.md` (section/library overviews) and `constants.md` (hand-authored
    constant tables) are excluded. `name` is the file stem, matched against module
    functions later; the nav label is free to differ (e.g. "noteToFreq()")."""
    if out is None:
        out = []
    for item in nav:
        _, value = parse_item(item)
        if isinstance(value, list):
            function_leaf_pages(value, out)
        elif isinstance(value, str) and value.endswith(".md"):
            stem = posixpath.basename(value)[:-len(".md")]
            if stem not in ("index", "constants"):
                out.append((stem, posixpath.dirname(value)))
    return out


def section_titles(nav, out=None):
    """{directory: title} for every section that owns an `…/index.md` (its Overview).
    Supplies the heading for a function library whose index lives at a section's own
    index (e.g. `api/utilities` -> "Mapping Values")."""
    if out is None:
        out = {}
    for item in nav:
        title, value = parse_item(item)
        if isinstance(value, list):
            own = first_index_dir(value)
            if own is not None and title is not None:
                out[own] = title
            section_titles(value, out)
    return out


# --- inheritance -------------------------------------------------------------

def base_name(expr):
    """Simple class name from a base expression (e.g. 'gui.Drawable' -> 'Drawable')."""
    return expr.split(".")[-1].strip()


def build_chain(name, registry):
    """Class data from `name` up its single-base chain; plus an unresolved base
    name if the chain hit something not in the registry."""
    chain, seen, unresolved = [], set(), None
    current = name
    while current and current not in seen:
        seen.add(current)
        cls = registry.get(current)
        if cls is None:
            unresolved = current
            break
        chain.append(cls)
        bases = cls["bases"]
        current = base_name(bases[0]) if bases else None
    return chain, unresolved


def resolved_methods(chain):
    """Methods across the chain, subclass first; first definition of a name wins.

    Each method's documentation group is resolved to the *base-most* one declared for
    that name (chain walked base→subclass, first non-empty section wins): a subclass
    override then inherits the canonical group from the class that introduced the
    member, so only genuinely new subclass methods need their own `# doc-group:` marker.
    """
    section_by_name = {}
    for cls in reversed(chain):
        for method in cls["methods"]:
            if method.get("section") and method["name"] not in section_by_name:
                section_by_name[method["name"]] = method["section"]

    ordered, seen = [], set()
    for cls in chain:
        for method in cls["methods"]:
            if method["name"] not in seen:
                seen.add(method["name"])
                ordered.append({**method, "section": section_by_name.get(method["name"])})
    return ordered


def resolved_constructor(chain):
    """The nearest constructor signature up the chain, or None."""
    for cls in chain:
        if cls["constructor"] is not None:
            return cls["constructor"]
    return None


# --- rendering helpers -------------------------------------------------------

def required_positional(sig):
    """Names of the required positional params (no default) — the bare-minimum call."""
    return [p["name"] for p in sig["params"] if p["default"] is None]


def format_default(default):
    if default is None:
        return "_required_"
    return f"`{default}`"


def argument_rows(sig, parsed):
    """(name, type, default, description) per argument: positionals, *args, kw-only,
    **kwargs. Type and description come from the docstring's Args block, falling back
    to the AST annotation when the docstring doesn't document the parameter."""
    docs = parsed["args"]

    def row(name, annotation, default):
        info = docs.get(name) or docs.get(name.lstrip("*")) or {}
        return (name, info.get("type") or annotation, default, info.get("desc", ""))

    rows = [row(p["name"], p.get("annotation"), format_default(p["default"]))
            for p in sig["params"]]
    if sig["vararg"]:
        rows.append(row(f"*{sig['vararg']}", None, ""))
    rows += [row(kw["name"], kw.get("annotation"), format_default(kw["default"]))
             for kw in sig["kwonly"]]
    if sig["kwarg"]:
        rows.append(row(f"**{sig['kwarg']}", None, ""))
    return rows


def display_annotation(annotation):
    """Prettify an annotation for the API guide using the ANNOTATION_DISPLAY swaps."""
    text = annotation
    for literal, replacement in ANNOTATION_DISPLAY.items():
        text = text.replace(literal, replacement)
    return text


def docstring_or_placeholder(docstring):
    return docstring if docstring else NO_DOCSTRING


def is_static(method):
    return method["kind"] in ("staticmethod", "classmethod")


def is_property(method):
    return method["kind"] == "property"


def tidy(text):
    return re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"


def collapse_paragraphs(text):
    """Reflow prose the way Markdown reads it: a single line break is just a soft wrap,
    so join it into a space; only a blank line starts a new paragraph. Lets source
    docstrings wrap their description however they like without forcing mid-sentence
    breaks onto the rendered page."""
    paragraphs = re.split(r"\n[ \t]*\n", text)
    reflowed = [re.sub(r"\s*\n\s*", " ", p).strip() for p in paragraphs]
    return "\n\n".join(p for p in reflowed if p)


def indefinite_article(word):
    """"a" or "an" for `word` — a quick vowel-letter check, enough for class names."""
    return "an" if word[:1].lower() in "aeiou" else "a"


def qualified(prefix, name):
    """`prefix.name`, or bare `name` when there's no prefix (module-level functions)."""
    return f"{prefix}.{name}" if prefix else name


# --- docstring parsing (Google style) ----------------------------------------

_SECTION_RE = re.compile(r"^(Args|Arguments|Parameters|Returns|Yields|Raises)\s*:\s*$")
_ARG_RE = re.compile(r"^(?P<name>\*{0,2}\w+)\s*\((?P<type>.*?)\)\s*:\s*(?P<desc>.*)$")


def parse_docstring(text):
    """Split a Google-style docstring into summary, extended description, Args and
    Returns. Entries read `name (type[, optional]): description`; the `, optional`
    marker is stripped off the type. A Raises section is ignored by design."""
    result = {"summary": "", "description": "", "args": {}, "returns": []}
    if not text:
        return result
    lines = text.split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        result["summary"] = lines[i].strip()
        i += 1

    section = None          # None == extended description; else "args"/"returns"/"ignore"
    description, args, returns, current = [], [], [], None
    for line in lines[i:]:
        stripped = line.strip()
        header = _SECTION_RE.match(stripped)
        if header:
            label = header.group(1)
            section = ("args" if label in ("Args", "Arguments", "Parameters")
                       else "returns" if label in ("Returns", "Yields") else "ignore")
            current = None
            continue
        if section is None:
            description.append(line)
        elif section in ("args", "returns"):
            match = _ARG_RE.match(stripped)
            if match:
                entry_type = match.group("type").strip()
                optional = entry_type.endswith("optional")
                if optional:
                    entry_type = re.sub(r",\s*optional$", "", entry_type).strip()
                current = {"name": match.group("name"), "type": entry_type,
                           "desc": match.group("desc").strip(), "optional": optional}
                (args if section == "args" else returns).append(current)
            elif stripped and current is not None:
                current["desc"] = (current["desc"] + " " + stripped).strip()

    result["description"] = collapse_paragraphs("\n".join(description))
    result["args"] = {entry["name"]: entry for entry in args}
    result["returns"] = returns
    return result


# --- cross-reference linking -------------------------------------------------
# Wrap an in-prose `name()` / `Class.name()` reference in a link to its page. The
# docstrings cite other members with empty parens (house style: "use mapValue()"),
# so this matches calls with no arguments only — never a signature or a numeric range.

def _identity(text):
    return text


_REF_PROTECT = re.compile(r"`[^`]*`|\[[^\]]*\]\([^)]*\)")   # inline code / existing links
_REF_TOKEN = re.compile(r"(?<![\w.])(?:(?P<qual>[A-Za-z_]\w*)\.)?(?P<name>[A-Za-z_]\w*)\(\)")


def _resolve_reference(qualifier, name, index, owner_class):
    """The page path a reference points at, or None to leave it as plain text.

    A qualified `Class.name()` resolves to that class's method. A bare `name()`
    resolves to a method of the current page's own class, else a module-level
    function, else a method that belongs to exactly one class; anything ambiguous
    (a bare method on several classes) or unknown is left unlinked.
    """
    if qualifier:
        return index["class_methods"].get((qualifier, name))
    if owner_class and (owner_class, name) in index["class_methods"]:
        return index["class_methods"][(owner_class, name)]
    if name in index["functions"]:
        return index["functions"][name]
    owners = index["method_owners"].get(name) or []
    if len(owners) == 1:
        return owners[0][1]
    return None


def make_linker(index, base_dir, current_file, owner_class):
    """Return a text transform that links references found in the prose of one page.
    base_dir is that page's directory (links are made relative to it); current_file is
    its own path (self-references stay plain); owner_class is the class the page
    documents, or None for a free-function page. Inline code and existing links are
    left untouched."""
    def link_segment(segment):
        def replace(match):
            target = _resolve_reference(match.group("qual"), match.group("name"),
                                        index, owner_class)
            if not target or target == current_file:
                return match.group(0)
            return f"[{match.group(0)}]({posixpath.relpath(target, base_dir)})"
        return _REF_TOKEN.sub(replace, segment)

    def link(text):
        if not text:
            return text
        out, pos = [], 0
        for protected in _REF_PROTECT.finditer(text):
            out.append(link_segment(text[pos:protected.start()]))
            out.append(protected.group(0))
            pos = protected.end()
        out.append(link_segment(text[pos:]))
        return "".join(out)

    return link


def full_call(sig):
    """Full argument list with defaults, e.g. 'timeInterval, action, parameters=None'."""
    parts = [p["name"] if p["default"] is None else f"{p['name']}={p['default']}"
             for p in sig["params"]]
    if sig["vararg"]:
        parts.append(f"*{sig['vararg']}")
    parts += [kw["name"] if kw["default"] is None else f"{kw['name']}={kw['default']}"
              for kw in sig["kwonly"]]
    if sig["kwarg"]:
        parts.append(f"**{sig['kwarg']}")
    return ", ".join(parts)


def arguments_block(call_target, sig, parsed, link=_identity, heading="Parameters"):
    """The arguments section: a `## <heading>` title, the full call, and a typed,
    described table. Empty when the signature takes no arguments. Method pages keep the
    default "Parameters"; a class page passes "Creating a <Class>" for its constructor."""
    rows = argument_rows(sig, parsed)
    if not rows:
        return []
    out = ["", f"## {heading}", "", "```python", f"{call_target}({full_call(sig)})", "```",
           "", "| Parameter | Type | Default | Description |", "|---|---|---|---|"]
    for name, annotation, default, desc in rows:
        type_cell = f"`{display_annotation(annotation)}`" if annotation else ""
        out.append(f"| `{name}` | {type_cell} | {default} | {link(desc)} |")
    return out


def returns_block(parsed, method, link=_identity):
    """The '## Returns' section, driven by the docstring; falls back to the AST return
    expressions for modules not yet migrated to the docstring format."""
    rets = parsed["returns"]
    if rets:
        out = ["", "## Returns", "", f"`return {', '.join(r['name'] for r in rets)}`",
               "", "| Value | Type | Description |", "|---|---|---|"]
        for r in rets:
            type_cell = f"`{display_annotation(r['type'])}`" if r["type"] else ""
            out.append(f"| {r['name']} | {type_cell} | {link(r['desc'])} |")
        return out
    meaningful = [r for r in (method.get("returns") or []) if r != "None"]
    if meaningful:
        return ["", "## Returns", "", "```python", "\n".join(meaningful), "```"]
    return []


# --- page builders -----------------------------------------------------------

def method_page(method, class_lower, class_upper, link=_identity):
    name = method["name"]
    prefix = class_upper if is_static(method) else class_lower
    parsed = parse_docstring(method.get("docstring"))
    summary = link(parsed["summary"]) or NO_DOCSTRING

    if is_property(method):
        lines = [f"# {name}", "", summary, "", "```python", qualified(prefix, name), "```"]
    else:
        call = ", ".join(required_positional(method))
        lines = [f"# {name}()", "", summary, "",
                 "```python", f"{qualified(prefix, name)}({call})", "```"]

    if parsed["description"]:
        lines += ["", link(parsed["description"])]
    if not is_property(method):
        lines += arguments_block(qualified(prefix, name), method, parsed, link)
    lines += returns_block(parsed, method, link)
    return tidy("\n".join(lines))


def method_table_row(method, prefix):
    name = method["name"]
    if is_property(method):
        target = qualified(prefix, name)
    else:
        call = ", ".join(required_positional(method))
        target = f"{qualified(prefix, name)}({call})"
    summary = parse_docstring(method.get("docstring"))["summary"] or ROW_DESC
    return f"| [`{target}`]({name}.md) | {summary} |"


def group_methods(methods):
    """Split instance methods into (ungrouped, [(label, methods), …]). Ungrouped methods
    (no `# doc-group:` marker — typically a class's own primary functions) keep source
    order; the labelled groups follow DOC_GROUP_ORDER, any extras appended in first-seen
    order. Each group keeps its members in resolved (source) order."""
    ungrouped, grouped = [], {}
    for method in methods:
        section = method.get("section")
        if section:
            grouped.setdefault(section, []).append(method)
        else:
            ungrouped.append(method)
    ordered_labels = [g for g in DOC_GROUP_ORDER if g in grouped]
    ordered_labels += [g for g in grouped if g not in DOC_GROUP_ORDER]
    return ungrouped, [(label, grouped[label]) for label in ordered_labels]


def class_index_page(class_name, chain, methods, link=_identity):
    class_lower = class_name.lower()
    constructor = resolved_constructor(chain)
    ctor_args = ", ".join(required_positional(constructor)) if constructor else ""

    properties = [m for m in methods if is_property(m)]
    statics = [m for m in methods if is_static(m)]
    instances = [m for m in methods if m["kind"] == "method"]

    parsed = parse_docstring(chain[0].get("docstring"))
    lines = [f"# {class_name}", "", link(parsed["summary"]) or NO_DOCSTRING]
    # A class with no constructor and only static methods is a namespace, not an
    # instantiable object — skip the "obj = Class()" usage line.
    if constructor is not None or instances:
        lines += ["", "```python", f"{class_lower} = {class_name}({ctor_args})", "```"]
    if parsed["description"]:
        lines += ["", link(parsed["description"])]
    if constructor:
        lines += arguments_block(class_name, constructor, parsed, link,
                                 heading=f"Creating {indefinite_article(class_name)} {class_name}")

    if properties:
        lines += ["", "## Properties", "", SECTION_DESC, "",
                  "| Property | Description |", "|---|---|"]
        for prop in properties:
            desc = parse_docstring(prop.get("docstring"))["summary"] or ROW_DESC
            lines.append(f"| [`{class_lower}.{prop['name']}`]({prop['name']}.md) | {desc} |")

    # Primary (headerless) table: ungrouped instance methods if any, otherwise the
    # static ones. Grouped instance methods follow as labelled `###` blocks.
    ungrouped, sections = group_methods(instances)
    primary = ungrouped if instances else statics
    primary_prefix = class_lower if instances else class_name
    if instances or statics:
        lines += ["", "## Functions"]
        if primary:
            lines += ["", "| Function | Description |", "|---|---|"]
            for method in primary:
                lines.append(method_table_row(method, primary_prefix))
        for label, members in sections:
            lines += ["", f"### {label}", "", "| Function | Description |", "|---|---|"]
            for method in members:
                lines.append(method_table_row(method, class_lower))

    # Separate "## Static Functions" only when the class has both kinds.
    if instances and statics:
        lines += ["", "## Static Functions", "", SECTION_DESC, "",
                  "| Function | Description |", "|---|---|"]
        for method in statics:
            lines.append(method_table_row(method, class_name))

    return tidy("\n".join(lines))


def module_index_page(title, functions):
    """Index page for a free-function library (a module with no classes): the nav
    title as heading, a description placeholder, and a table of its functions.
    Mirrors a class index but without an object/constructor; the functions are
    module-level, so their calls carry no prefix."""
    lines = [f"# {title}", "", SECTION_DESC]
    if functions:
        lines += ["", "## Functions", "", "| Function | Description |", "|---|---|"]
        for function in functions:
            lines.append(method_table_row(function, ""))
    return tidy("\n".join(lines))


# --- main --------------------------------------------------------------------

def load_registry(json_dir):
    registry = {}
    for path in sorted(json_dir.glob("*.json")):
        if path.name.endswith("_constants.json"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for cls in data.get("classes", []):
            registry[cls["name"]] = cls
    return registry


def load_function_modules(json_dir):
    """Free-function libraries — modules that expose functions and no classes — as
    (module_stem, functions). These get an index page. A module that also has classes
    is represented by those classes; any of its module-level functions still render
    individually when the nav advertises them (see load_all_functions)."""
    modules = []
    for path in sorted(json_dir.glob("*.json")):
        if path.name.endswith("_constants.json"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("classes"):
            continue
        functions = data.get("functions") or []
        if functions:
            modules.append((data["module"], functions))
    return modules


def load_all_functions(json_dir):
    """Every module-level function across all modules, as name -> (module_stem, func).
    Used to resolve the per-function pages the nav advertises, including functions in
    modules that also define classes (e.g. music.noteToFreq)."""
    found = {}
    for path in sorted(json_dir.glob("*.json")):
        if path.name.endswith("_constants.json"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for func in data.get("functions") or []:
            found[func["name"]] = (data["module"], func)
    return found


def build_reference_index(registry, by_title, by_basename, nav_functions,
                          all_functions, function_modules):
    """Map every member that gets a page to that page's path, for cross-linking prose.

    Mirrors the placement decisions the render loops make, but read-only and ahead of
    them, so a reference can point at a member generated later. Returns:
        functions      name -> page path
        class_methods  (Class, method) -> page path
        method_owners  method -> [(Class, page path)]  (a length of 1 means unique)
        classes        Class -> index page path
    """
    functions, class_methods, method_owners, classes = {}, {}, {}, {}

    for name in sorted(registry):
        directory = locate_class(name, by_title, by_basename)
        if directory is None:
            continue
        chain, _ = build_chain(name, registry)
        classes[name] = posixpath.join(directory, "index.md")
        for method in resolved_methods(chain):
            path = posixpath.join(directory, method["name"] + ".md")
            class_methods[(name, method["name"])] = path
            method_owners.setdefault(method["name"], []).append((name, path))

    advertised_stems = set()
    for name, directory in nav_functions:
        match = all_functions.get(name)
        if match is None:
            continue
        advertised_stems.add(match[0])
        functions[name] = posixpath.join(directory, name + ".md")

    for stem, funcs in function_modules:
        if stem in advertised_stems:
            continue
        directory = by_basename.get(stem.lower())
        if directory is None:
            continue
        for func in funcs:
            functions[func["name"]] = posixpath.join(directory, func["name"] + ".md")

    return {"functions": functions, "class_methods": class_methods,
            "method_owners": method_owners, "classes": classes}


def main():
    if len(sys.argv) != 5:
        print("usage: python style_api.py <mkdocs.yml> <json_dir> <target_dir> <mode>",
              file=sys.stderr)
        print(f"  mode is one of: {', '.join(sorted(MODES))}", file=sys.stderr)
        sys.exit(1)

    config_path, json_raw, target_raw, mode = sys.argv[1:5]
    if mode not in MODES:
        print(f"error: mode must be one of {sorted(MODES)} (got {mode!r})", file=sys.stderr)
        sys.exit(1)
    write_classes = mode != "methods"

    config_path = Path(config_path).expanduser()
    json_dir = Path(json_raw).expanduser()
    target_dir = Path(target_raw).expanduser()
    for label, path in [("mkdocs.yml", config_path), ("json_dir", json_dir)]:
        if not path.exists():
            print(f"error: {label} not found: {path}", file=sys.stderr)
            sys.exit(1)

    config = yaml.load(config_path.read_text(encoding="utf-8"), Loader=_Loader) or {}
    nav = config.get("nav") or []
    by_title, by_basename, by_directory_title = class_dir_lookup(nav)
    titles_by_dir = section_titles(nav)
    nav_functions = function_leaf_pages(nav)        # (name, directory) per advertised page
    registry = load_registry(json_dir)
    function_modules = load_function_modules(json_dir)
    all_functions = load_all_functions(json_dir)
    reference_index = build_reference_index(registry, by_title, by_basename,
                                            nav_functions, all_functions, function_modules)

    generated_classes = 0
    generated_modules = 0
    method_pages = 0
    missing_from_nav = []
    unresolved_bases = {}

    for name in sorted(registry):
        directory = locate_class(name, by_title, by_basename)
        if directory is None:
            missing_from_nav.append(name)
            continue

        chain, unresolved = build_chain(name, registry)
        if unresolved:
            unresolved_bases.setdefault(unresolved, []).append(name)

        methods = resolved_methods(chain)
        out_dir = target_dir / directory
        out_dir.mkdir(parents=True, exist_ok=True)

        if write_classes:
            link = make_linker(reference_index, directory,
                               posixpath.join(directory, "index.md"), name)
            (out_dir / "index.md").write_text(
                class_index_page(name, chain, methods, link), encoding="utf-8")
            generated_classes += 1

        for method in methods:
            link = make_linker(reference_index, directory,
                               posixpath.join(directory, method["name"] + ".md"), name)
            (out_dir / f"{method['name']}.md").write_text(
                method_page(method, name.lower(), name, link), encoding="utf-8")
            method_pages += 1

    # Per-function pages the nav advertises (a `<dir>/<name>.md` leaf). These can be
    # functions of a class-bearing module (e.g. music.noteToFreq) — the nav decides
    # which appear and where; functions it omits (e.g. mapScale) are simply not built.
    # advertised: module_stem -> [(name, directory), ...] in nav order, for the indexes.
    advertised = {}
    for name, directory in nav_functions:
        match = all_functions.get(name)
        if match is None:
            continue                 # a content page (download, constants, …), not a function
        stem, function = match
        advertised.setdefault(stem, []).append((name, directory))
        out_dir = target_dir / directory
        out_dir.mkdir(parents=True, exist_ok=True)
        link = make_linker(reference_index, directory,
                           posixpath.join(directory, name + ".md"), None)
        (out_dir / f"{name}.md").write_text(
            method_page(function, "", "", link), encoding="utf-8")
        method_pages += 1

    # Function-library index pages (a module with no classes, e.g. utilities, zipf).
    # When the nav advertises the library's functions individually, the index lists
    # exactly those (in nav order), and their pages were already written above. When it
    # lists only the library's Overview, every function is generated and listed here.
    for stem, functions in function_modules:
        shown = advertised.get(stem)
        if shown:
            dirs = {directory for _, directory in shown}
            directory = posixpath.commonpath(list(dirs)) if len(dirs) > 1 else dirs.pop()
            by_name = {function["name"]: function for function in functions}
            listed = [by_name[name] for name, _ in shown if name in by_name]
        else:
            directory = by_basename.get(stem.lower())
            if directory is None:
                missing_from_nav.append(stem)
                continue
            listed = functions
            out_dir = target_dir / directory
            out_dir.mkdir(parents=True, exist_ok=True)
            for function in functions:
                link = make_linker(reference_index, directory,
                                   posixpath.join(directory, function["name"] + ".md"), None)
                (out_dir / f"{function['name']}.md").write_text(
                    method_page(function, "", "", link), encoding="utf-8")
                method_pages += 1

        if write_classes:
            out_dir = target_dir / directory
            out_dir.mkdir(parents=True, exist_ok=True)
            title = (titles_by_dir.get(directory) or by_directory_title.get(directory)
                     or stem.capitalize())
            (out_dir / "index.md").write_text(
                module_index_page(title, listed), encoding="utf-8")
            generated_modules += 1

    print(f"mode: {mode}")
    if write_classes:
        print(f"Wrote {generated_classes} class index file(s), {generated_modules} "
              f"function-library index file(s) and {method_pages} method/function page(s)")
    else:
        print(f"Wrote {method_pages} method/function page(s)")

    # A class is "missing" either because it is intentionally out of the nav (an
    # abstract base, a deprecated module) or because it was given a flat `<class>.md`
    # page instead of a `<class>/index.md` directory — split the two so the second,
    # which is a real mistake, stands out.
    flat_leaves = {name.lower(): posixpath.join(directory, name + ".md")
                   for name, directory in nav_functions}
    classes_as_flat = [(name, flat_leaves[name.lower()])
                       for name in missing_from_nav if name.lower() in flat_leaves]
    genuinely_missing = [name for name in missing_from_nav
                         if name.lower() not in flat_leaves]

    if genuinely_missing:
        print(f"\nClasses/modules in the JSON but not in the nav ({len(genuinely_missing)}) "
              "— no pages generated (expected for abstract bases and deprecated modules):")
        for name in genuinely_missing:
            print(f"  {name}")

    if classes_as_flat:
        print(f"\nClasses given a flat page in the nav ({len(classes_as_flat)}) "
              "— use a `<class>/index.md` directory so method pages can be generated:")
        for name, page in classes_as_flat:
            print(f"  {name}  ->  {page}")

    if unresolved_bases:
        print(f"\nUnresolved base classes ({len(unresolved_bases)}) "
              "— inheritance chain stopped here:")
        for base, subclasses in sorted(unresolved_bases.items()):
            print(f"  {base}  (referenced by: {', '.join(sorted(subclasses))})")


if __name__ == "__main__":
    main()
