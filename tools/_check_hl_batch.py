# -*- coding: utf-8 -*-
"""Count bodies in highlight generator modules."""
from __future__ import annotations

import importlib.util
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def check(book_id: str, title: str, author: str, bodies: list[str]) -> None:
    print(f"{book_id}: {len(bodies)}")
    if len(bodies) != 150:
        print("  COUNT ERROR")
    short = [b for b in bodies if len(b) < 12]
    if short:
        print("  short", len(short), short[:2])
    for f in ("本書", "作者指出", "本章", "這一章", "｜"):
        hits = [b for b in bodies if f in b]
        if hits:
            print("  forbidden", f, len(hits))
    if len(set(bodies)) != len(bodies):
        print("  DUP bodies", len(bodies) - len(set(bodies)))
    c = Counter(b[:18] for b in bodies if len(b) >= 18)
    bad = [(k, v) for k, v in c.most_common(5) if v >= 4]
    if bad:
        print("  repeated starts", bad)
    # colon tags
    short_colon = 0
    for b in bodies:
        m = re.match(r"^([^：:]{1,12})[：:]", b)
        if m and not m.group(1).endswith(("是", "為", "在於", "說", "問", "提醒", "表示", "指出")):
            short_colon += 1
    if short_colon:
        print("  short_colon", short_colon)
    # simplified heuristics
    simp = [b for b in bodies if re.search(r"[这说过门见风干发会体显经]", b)]
    # too noisy; skip


def main() -> None:
    for fn in sorted(Path(ROOT / "tools").glob("_gen_grok_20260719_hl_p*.py")):
        mod = load(fn.stem, fn)
        for book_id, (title, author, bodies) in mod.BOOKS.items():
            check(book_id, title, author, bodies)


if __name__ == "__main__":
    main()
