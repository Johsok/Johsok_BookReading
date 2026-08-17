# -*- coding: utf-8 -*-
"""Validate highlight generators and print counts."""
from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

try:
    import zhconv
except ImportError:
    zhconv = None


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def extra_checks(mod, start_word: str, max_start: int, author: str) -> list[str]:
    errs = []
    bodies = list(mod.BODIES)
    if len(bodies) != 150:
        errs.append(f"count={len(bodies)}")
    starts = Counter(b[:18] for b in bodies)
    bad = [(k, n) for k, n in starts.items() if n >= 4]
    if bad:
        errs.append(f"repeat18={bad[:5]}")
    n_start = sum(1 for b in bodies if b.startswith(start_word))
    if n_start >= max_start:
        errs.append(f"start {start_word}={n_start}")
    n_author = sum(author in b for b in bodies)
    if n_author >= 2:
        errs.append(f"author={n_author}")
    if zhconv:
        diffs = []
        for i, b in enumerate(bodies, 1):
            trad = zhconv.convert(b, "zh-hant")
            if trad != b:
                diffs.append(i)
        if diffs:
            errs.append(f"zhconv_lines={diffs[:20]} n={len(diffs)}")
    for i, b in enumerate(bodies, 1):
        if any(x in b for x in ("本書", "作者指出", "本章", "這一章", "｜")):
            errs.append(f"forbidden@{i}")
    return errs


def main() -> None:
    files = [
        (TOOLS / "_hl_redo_07_other-20260716-53.py", "共濟會", 15, "沈以謙"),
        (TOOLS / "_hl_redo_07_other-20260716-54.py", "曾國藩", 75, "趙焰"),
    ]
    for path, start_word, max_start, author in files:
        print("==", path.name)
        mod = load(path)
        errs = extra_checks(mod, start_word, max_start, author)
        if errs:
            print("EXTRA", errs)
        mod.main()
        print("OK")


if __name__ == "__main__":
    main()
