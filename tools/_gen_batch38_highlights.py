# -*- coding: utf-8 -*-
"""Generate findbook results JSON for batch38 food wellness books."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def numbered(lines: list[str]) -> list[str]:
    assert len(lines) == 150, len(lines)
    out = []
    for i, body in enumerate(lines, 1):
        body = body.strip()
        assert len(body) >= 12, (i, body)
        out.append(f"{i:03d}、{body}")
    return out


def write_results(book_id: str, lines: list[str]) -> Path:
    path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    payload = {"id": book_id, "highlights": numbered(lines)}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def run_writer(category_id: str, results_path: Path) -> None:
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "findbook_writer.py"),
        "complete",
        "--category-id",
        category_id,
        "--results",
        str(results_path),
    ]
    print("RUN", " ".join(cmd))
    subprocess.run(cmd, cwd=str(ROOT), check=True)


def load_bodies(name: str) -> list[str]:
    """Load highlight bodies from sibling text file (one body per line)."""
    path = ROOT / "tools" / f"_batch38_{name}.txt"
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if len(lines) != 150:
        raise SystemExit(f"{path.name} has {len(lines)} lines, need 150")
    return lines


def main() -> None:
    mapping = [
        ("05_food_wellness-20260718-16", "05_food_wellness", "h16"),
        ("05_food_wellness-20260718-17", "05_food_wellness", "h17"),
        ("05_food_wellness-20260718-18", "05_food_wellness", "h18"),
        ("05_food_wellness-20260718-19", "05_food_wellness", "h19"),
        ("05_food_wellness-20260718-20", "05_food_wellness", "h20"),
    ]
    ok, fail = [], []
    for book_id, category_id, key in mapping:
        try:
            bodies = load_bodies(key)
            path = write_results(book_id, bodies)
            run_writer(category_id, path)
            ok.append(book_id)
        except Exception as e:
            fail.append((book_id, str(e)))
            print(f"FAIL {book_id}: {e}", file=sys.stderr)
    print("OK:", ok)
    print("FAIL:", fail)
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
