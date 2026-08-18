# -*- coding: utf-8 -*-
"""Merge extras and overwrite JSON highlights."""
import ast
import importlib.util
from pathlib import Path

from _tmp_ns_hl_extra import EXTRA
from _tmp_ns_hl_patch import patch

ROOT = Path(__file__).resolve().parent


def load_items(filename):
    src = (ROOT / filename).read_text(encoding="utf-8")
    mod = ast.parse(src)
    for node in mod.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "ITEMS":
                    return list(ast.literal_eval(node.value))
    raise SystemExit(f"no ITEMS in {filename}")


def load_summary(filename):
    src = (ROOT / filename).read_text(encoding="utf-8")
    mod = ast.parse(src)
    for node in ast.walk(mod):
        if isinstance(node, ast.Call):
            func = node.func
            name = getattr(func, "id", None) or getattr(func, "attr", None)
            if name == "patch" and len(node.args) >= 3:
                arg = node.args[2]
                if isinstance(arg, ast.Constant):
                    return arg.value
                if isinstance(arg, ast.Str):
                    return arg.s
            if name == "patch" and node.keywords:
                for kw in node.keywords:
                    if kw.arg == "summary":
                        v = kw.value
                        if isinstance(v, ast.Constant):
                            return v.value
                        if isinstance(v, ast.Str):
                            return v.s
    return None


BOOKS = [
    ("81", "03_natural_science-20260716-81.json", "_tmp_write_hl_81.py"),
    ("92", "03_natural_science-20260716-92.json", "_tmp_write_hl_92.py"),
    ("93", "03_natural_science-20260716-93.json", "_tmp_write_hl_93.py"),
    ("94", "03_natural_science-20260716-94.json", "_tmp_write_hl_94.py"),
    ("95", "03_natural_science-20260716-95.json", "_tmp_write_hl_95.py"),
    ("96", "03_natural_science-20260716-96.json", "_tmp_write_hl_96.py"),
    ("97", "03_natural_science-20260716-97.json", "_tmp_write_hl_97.py"),
    ("98", "03_natural_science-20260716-98.json", "_tmp_write_hl_98.py"),
    ("99", "03_natural_science-20260716-99.json", "_tmp_write_hl_99.py"),
]


def main():
    for key, json_name, py_name in BOOKS:
        items = load_items(py_name)
        extra = EXTRA.get(key, [])
        merged = items + extra
        if len(merged) != 150:
            raise SystemExit(f"{key}: got {len(merged)} from {len(items)}+{len(extra)}")
        if len(set(merged)) != 150:
            raise SystemExit(f"{key}: duplicates")
        summary = load_summary(py_name)
        patch(json_name, merged, summary=summary)


if __name__ == "__main__":
    main()
