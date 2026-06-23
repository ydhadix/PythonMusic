#!/usr/bin/env python3
"""Extract a semi-structured API inventory from Python source files.

Each .py file directly in the target folder is parsed with the `ast` module
(no imports, no code execution) and its public API is written as JSON to ./api/
(relative to the current working directory).

Usage:
    python extract_api.py <folder>
    python extract_api.py            # prompts for the folder

For every source file <name>.py we write:
    api/<name>.json            classes (constructor, constants, methods) + free functions
    api/<name>_constants.json  free (module-level) constants, only if there are any

Captured per callable: its docstring, argument names, defaults, and any
annotations, plus the returned expression(s) read from the `return` statements.
Each class also captures its own docstring (the constructor's docstring is not
captured). Names beginning with "_" are treated as private and skipped (except
__init__, used for the constructor). Existing files in api/ that we don't
regenerate are left alone.
"""

import ast
import io
import json
import re
import sys
import tokenize
from pathlib import Path


# A `# doc-group: <Label>` comment in a class body opens a documentation group: every
# method defined after it (until the next marker) belongs to that group, so the API
# guide can split a class's functions into labelled `###` blocks (Position, Size, …).
# `# doc-group: none` closes the current group (the methods that follow are ungrouped).
# Comments carry no AST node, so the markers are read from the token stream by line.
_DOC_GROUP_RE = re.compile(r"^#\s*doc-group:\s*(.+?)\s*$")


def is_public(name):
    return not name.startswith("_")


def doc_group_markers(source):
    """Sorted [(lineno, label)] for every `# doc-group:` comment; label None for `none`."""
    markers = []
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    try:
        for token in tokens:
            if token.type == tokenize.COMMENT:
                match = _DOC_GROUP_RE.match(token.string.strip())
                if match:
                    label = match.group(1)
                    markers.append((token.start[0], None if label.lower() == "none" else label))
    except tokenize.TokenError:
        pass  # an unterminated construct late in the file; markers gathered so far stand
    return markers


def group_at(line, class_start, markers):
    """The doc-group label in effect for a member defined at `line` within its class:
    the nearest marker between the class header and the member, or None."""
    label = None
    for marker_line, marker_label in markers:
        if class_start < marker_line < line:
            label = marker_label
        elif marker_line >= line:
            break
    return label


def unparse(node):
    """Return a node's source text, or None for a missing node."""
    if node is None:
        return None
    return ast.unparse(node)


def decorator_names(func):
    """Bare names of a function's decorators (e.g. 'staticmethod', 'property')."""
    names = []
    for decorator in func.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if isinstance(target, ast.Name):
            names.append(target.id)
        elif isinstance(target, ast.Attribute):
            names.append(target.attr)
    return names


def method_kind(func):
    decorators = decorator_names(func)
    if "staticmethod" in decorators:
        return "staticmethod"
    if "classmethod" in decorators:
        return "classmethod"
    if "property" in decorators:
        return "property"
    return "method"


def extract_signature(func, drop_first=False):
    """Arguments of a function/method as {params, vararg, kwonly, kwarg}."""
    args = func.args

    positional = list(args.posonlyargs) + list(args.args)
    # defaults align to the tail of the positional arguments
    padded_defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)
    params = [
        {"name": arg.arg, "annotation": unparse(arg.annotation), "default": unparse(default)}
        for arg, default in zip(positional, padded_defaults)
    ]
    if drop_first and params:  # drop self / cls
        params = params[1:]

    keyword_only = [
        {"name": arg.arg, "annotation": unparse(arg.annotation), "default": unparse(default)}
        for arg, default in zip(args.kwonlyargs, args.kw_defaults)
    ]

    return {
        "params": params,
        "vararg": args.vararg.arg if args.vararg else None,
        "kwonly": keyword_only,
        "kwarg": args.kwarg.arg if args.kwarg else None,
    }


class _ReturnCollector(ast.NodeVisitor):
    """Collect `return` expressions, without descending into nested scopes."""

    def __init__(self):
        self.returns = []

    def visit_Return(self, node):
        self.returns.append("None" if node.value is None else ast.unparse(node.value))

    # do not look inside nested functions / classes / lambdas
    def visit_FunctionDef(self, node):
        pass

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        pass

    def visit_Lambda(self, node):
        pass


def extract_returns(func):
    collector = _ReturnCollector()
    for statement in func.body:
        collector.visit(statement)
    unique = []
    for expression in collector.returns:
        if expression not in unique:
            unique.append(expression)
    return unique


def extract_callable(func, kind, section=None):
    drop_first = kind in ("method", "classmethod", "property")
    return {
        "name": func.name,
        "kind": kind,
        "section": section,
        "docstring": ast.get_docstring(func),
        **extract_signature(func, drop_first=drop_first),
        "returns": extract_returns(func),
    }


def assignment_constants(node):
    """(name, value) pairs from an Assign, handling tuple and chained targets."""
    pairs = []
    value = node.value
    for target in node.targets:
        if isinstance(target, (ast.Tuple, ast.List)):
            names = target.elts
            if isinstance(value, (ast.Tuple, ast.List)) and len(value.elts) == len(names):
                values = value.elts
            else:
                values = [value] * len(names)
        else:
            names = [target]
            values = [value]
        for name_node, value_node in zip(names, values):
            if isinstance(name_node, ast.Name) and is_public(name_node.id):
                pairs.append((name_node.id, unparse(value_node)))
    return pairs


def annotated_constant(node):
    """(name, value) for an AnnAssign target, or None."""
    if isinstance(node.target, ast.Name) and is_public(node.target.id):
        return node.target.id, unparse(node.value)
    return None


def extract_class(cls, markers=()):
    constructor = None
    constants = []
    methods = []
    for node in cls.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == "__init__":
                constructor = extract_signature(node, drop_first=True)
            elif is_public(node.name):
                section = group_at(node.lineno, cls.lineno, markers)
                methods.append(extract_callable(node, method_kind(node), section))
        elif isinstance(node, ast.Assign):
            constants.extend({"name": n, "value": v} for n, v in assignment_constants(node))
        elif isinstance(node, ast.AnnAssign):
            entry = annotated_constant(node)
            if entry:
                constants.append({"name": entry[0], "value": entry[1]})
    return {
        "name": cls.name,
        "docstring": ast.get_docstring(cls),
        "bases": [unparse(base) for base in cls.bases],
        "constructor": constructor,
        "constants": constants,
        "methods": methods,
    }


def extract_module(tree, markers=()):
    classes, functions, constants = [], [], []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if is_public(node.name):
                functions.append(extract_callable(node, "function"))
        elif isinstance(node, ast.ClassDef):
            if is_public(node.name):
                classes.append(extract_class(node, markers))
        elif isinstance(node, ast.Assign):
            constants.extend({"name": n, "value": v} for n, v in assignment_constants(node))
        elif isinstance(node, ast.AnnAssign):
            entry = annotated_constant(node)
            if entry:
                constants.append({"name": entry[0], "value": entry[1]})
    return classes, functions, constants


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    if len(sys.argv) > 1:
        raw_target = sys.argv[1]
    else:
        raw_target = input("Path to the folder to extract: ").strip()

    target = Path(raw_target).expanduser()
    if not target.is_dir():
        print(f"error: not a directory: {target}", file=sys.stderr)
        sys.exit(1)

    source_files = sorted(p for p in target.iterdir() if p.is_file() and p.suffix == ".py")
    if not source_files:
        print(f"No .py files found directly in {target}")
        return

    output_dir = Path("_api_data")
    output_dir.mkdir(parents=True, exist_ok=True)

    written = []
    skipped = []
    for source in source_files:
        text = source.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text, filename=str(source))
        except SyntaxError as error:
            print(f"skip (syntax error): {source} -> {error}", file=sys.stderr)
            skipped.append(source.name)
            continue

        markers = doc_group_markers(text)
        classes, functions, constants = extract_module(tree, markers)
        stem = source.stem

        write_json(output_dir / f"{stem}.json", {
            "module": stem,
            "source": str(source),
            "classes": classes,
            "functions": functions,
        })
        written.append(f"{stem}.json")

        if constants:
            write_json(output_dir / f"{stem}_constants.json", {
                "module": stem,
                "source": str(source),
                "constants": constants,
            })
            written.append(f"{stem}_constants.json")

    print(f"Processed {len(source_files)} file(s) from {target}")
    print(f"Wrote {len(written)} file(s) to {output_dir}/:")
    for name in written:
        print(f"  {name}")
    if skipped:
        print(f"Skipped {len(skipped)}: {', '.join(skipped)}")


if __name__ == "__main__":
    main()
