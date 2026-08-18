# -*- coding: utf-8 -*-
"""Atomically write chatgptHighlights for 06_computer_info 70, 71, 01, 02."""
from __future__ import annotations

import importlib.util
import json
import os
import re
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
BOOKS = ROOT / "Books" / "06_computer_info"
TMP = ROOT / "_tmp"
STAMP = "2026-08-18T08:58:00+08:00"
UPDATED = "2026-08-18"

BANNED = ("本書", "作者指出", "本章", "這一章", "｜")
COLON_RE = re.compile(r"[：:]")
STEP_RE = re.compile(r".*面第\d+步")


def _load_hl(module_path: Path) -> list[str]:
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    hl = list(mod.HL)
    assert len(hl) == 150, f"{module_path.name} count={len(hl)}"
    return hl


def _numbered(bodies: list[str]) -> list[str]:
    return [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]


def _validate(name: str, lines: list[str]) -> None:
    assert len(lines) == 150, f"{name} len={len(lines)}"
    bodies = []
    starts = []
    for i, line in enumerate(lines, 1):
        prefix = f"{i:03d}、"
        assert line.startswith(prefix), f"{name} bad prefix {i}: {line[:30]}"
        body = line[len(prefix) :]
        assert body.strip(), f"{name} empty {i}"
        for b in BANNED:
            assert b not in line, f"{name} banned {b} in {i}"
        assert not STEP_RE.search(line), f"{name} step pattern {i}"
        # 少用冒號：允許極少數技術必要時，但整批應接近零
        bodies.append(body)
        starts.append(body[:4] if len(body) >= 4 else body)
    assert len(set(lines)) == 150, f"{name} duplicate lines"
    assert len(set(bodies)) == 150, f"{name} duplicate bodies"
    top = Counter(starts).most_common(3)
    for s, c in top:
        assert c <= 3, f"{name} repeated openings {s!r} x{c}"
    colon_n = sum(1 for line in lines if COLON_RE.search(line))
    assert colon_n <= 5, f"{name} too many colons: {colon_n}"


def _write(path: Path, highlights: list[str]) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    data["chatgptHighlights"] = highlights
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = UPDATED
    raw = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(suffix=".json", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(raw)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
    check = json.loads(path.read_text(encoding="utf-8-sig"))
    return check


def main() -> None:
    jobs = [
        ("06_computer_info-20260716-70.json", TMP / "hl_b70_python.py"),
        ("06_computer_info-20260716-71.json", TMP / "hl_b71_llmops.py"),
        ("06_computer_info-20260717-01.json", TMP / "hl_b01_cnapp.py"),
        ("06_computer_info-20260717-02.json", TMP / "hl_b02_sideproject.py"),
    ]
    results = []
    for fname, mod_path in jobs:
        bodies = _load_hl(mod_path)
        lines = _numbered(bodies)
        _validate(fname, lines)
        path = BOOKS / fname
        check = _write(path, lines)
        hs = check["chatgptHighlights"]
        ok = (
            len(hs) == 150
            and check.get("chatgptStatus") == "complete"
            and check.get("highlightsSource") == "grok"
            and check.get("updatedAt") == UPDATED
            and check.get("highlightsCapturedAt") == STAMP
            and hs[0].startswith("001、")
            and hs[-1].startswith("150、")
        )
        results.append((fname, len(hs), ok))
        print(f"{fname}\tcount={len(hs)}\tok={ok}")
        print(f"  FIRST: {hs[0][:60]}...")
        print(f"  LAST:  {hs[-1][:60]}...")
    failed = [r for r in results if not r[2]]
    if failed:
        raise SystemExit(f"FAILED: {failed}")
    print("ALL_OK", len(results))


if __name__ == "__main__":
    main()
