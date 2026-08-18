# -*- coding: utf-8 -*-
"""Overwrite chatgptHighlights for 05_food_wellness-20260716-51..60."""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
BOOKS = ROOT / "Books" / "05_food_wellness"
TMP = ROOT / "_tmp"
UPDATED = "2026-08-18"
CAPTURED = "2026-08-18T10:20:00+08:00"
BANNED = ("本書", "作者指出", "本章", "這一章", "｜")
STEP_RE = re.compile(r".面第\d+步")


def load_mod(name: str):
    path = TMP / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def validate(name: str, items: list[str]) -> None:
    if len(items) != 150:
        raise SystemExit(f"{name}: count {len(items)}")
    for i, t in enumerate(items, 1):
        if not t or t.startswith(("0", "1")) and "、" in t[:4]:
            raise SystemExit(f"{name}: numbered item at {i}: {t[:40]}")
        for b in BANNED:
            if b in t:
                raise SystemExit(f"{name}:{i} banned {b}")
        if STEP_RE.search(t):
            raise SystemExit(f"{name}:{i} step label")
    if len(set(items)) != 150:
        raise SystemExit(f"{name}: duplicate lines")

    def cjk_prefix(s: str, n: int = 8) -> str:
        chars = re.findall(r"[\u4e00-\u9fff]", s)
        return "".join(chars[:n])

    open_c = Counter(cjk_prefix(t) for t in items if cjk_prefix(t))
    bad = [(k, v) for k, v in open_c.items() if v >= 4]
    if bad:
        raise SystemExit(f"{name}: repeated openings: {bad[:5]}")
    starts = Counter(t[:18] for t in items if len(t) >= 18)
    if starts and starts.most_common(1)[0][1] >= 4:
        raise SystemExit(f"{name}: repeated 18-prefix {starts.most_common(1)[0]}")


def atomic_write(path: Path, data: dict) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def write_book(filename: str, highlights: list[str]) -> dict:
    path = BOOKS / filename
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)
    numbered = [f"{i:03d}、{t}" for i, t in enumerate(highlights, 1)]
    data["chatgptHighlights"] = numbered
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = CAPTURED
    data["updatedAt"] = UPDATED
    atomic_write(path, data)
    with path.open("r", encoding="utf-8-sig") as f:
        check = json.load(f)
    ok = (
        len(check["chatgptHighlights"]) == 150
        and check["chatgptHighlights"][0].startswith("001、")
        and check["chatgptHighlights"][-1].startswith("150、")
    )
    return {"file": filename, "title": data.get("title"), "count": len(check["chatgptHighlights"]), "ok": ok}


def main() -> None:
    m51 = load_mod("h51_52")
    m53 = load_mod("h53_54")
    m55 = load_mod("h55_56")
    m57 = load_mod("h57_58")
    m59 = load_mod("h59_60")
    books = [
        ("05_food_wellness-20260716-51.json", m51.BOOK51),
        ("05_food_wellness-20260716-52.json", m51.BOOK52),
        ("05_food_wellness-20260716-53.json", m53.BOOK53),
        ("05_food_wellness-20260716-54.json", m53.BOOK54),
        ("05_food_wellness-20260716-55.json", m55.BOOK55),
        ("05_food_wellness-20260716-56.json", m55.BOOK56),
        ("05_food_wellness-20260716-57.json", m57.BOOK57),
        ("05_food_wellness-20260716-58.json", m57.BOOK58),
        ("05_food_wellness-20260716-59.json", m59.BOOK59),
        ("05_food_wellness-20260716-60.json", m59.BOOK60),
    ]
    results = []
    for name, items in books:
        validate(name, items)
        results.append(write_book(name, items))
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
