# -*- coding: utf-8 -*-
"""Batch14: generate 150 highlights per book, validate, write via findbook_writer."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402


def numbered(bodies: list[str]) -> list[str]:
    return [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]


def save_and_complete(book_id: str, category_id: str, bodies: list[str]) -> str:
    if len(bodies) != 150:
        raise SystemExit(f"{book_id}: got {len(bodies)}, need 150")
    # drop accidental empties / fix short
    bodies = [b.strip() for b in bodies]
    for i, b in enumerate(bodies):
        if len(b) < 12:
            raise SystemExit(f"{book_id} line {i+1} too short: {b!r}")
    highlights = numbered(bodies)
    validate_highlights(book_id, highlights)
    path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    path.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "findbook_writer.py"),
        "complete",
        "--category-id",
        category_id,
        "--results",
        str(path),
    ]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8")
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        raise SystemExit(f"FAIL {book_id}:\n{out}")
    return f"OK {book_id}\n{out.strip()}"


def load_json_bodies(name: str) -> list[str]:
    path = ROOT / "tools" / f"_batch14_bodies_{name}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"{name} bodies must be list")
    return data


def main() -> None:
    books = [
        ("01_business_startup-20260718-41", "01_business_startup", "41"),
        ("01_business_startup-20260718-42", "01_business_startup", "42"),
        ("01_business_startup-20260718-43", "01_business_startup", "43"),
        ("01_business_startup-20260718-44", "01_business_startup", "44"),
        ("01_business_startup-20260718-45", "01_business_startup", "45"),
    ]
    results = []
    for book_id, cat, key in books:
        bodies = load_json_bodies(key)
        results.append(save_and_complete(book_id, cat, bodies))
    print("\n".join(results))


if __name__ == "__main__":
    main()
