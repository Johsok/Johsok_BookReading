# -*- coding: utf-8 -*-
"""Build and write batch43 highlights for all 5 books."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from _batch43_bodies import BODIES  # noqa: E402


def numbered(bodies: list[str]) -> list[str]:
    return [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]


def write_and_complete(book_id: str, category_id: str, bodies: list[str]) -> None:
    bodies = [b.strip() for b in bodies]
    if len(bodies) != 150:
        raise ValueError(f"{book_id} need 150, got {len(bodies)}")
    if len(set(bodies)) != 150:
        raise ValueError(f"{book_id} has duplicate bodies")
    for b in bodies:
        if len(b) < 12:
            raise ValueError(f"{book_id} body too short: {b}")
    results_path = TOOLS / f".findbook_results_grok_{book_id}.json"
    payload = {"id": book_id, "highlights": numbered(bodies)}
    results_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        str(TOOLS / "findbook_writer.py"),
        "complete",
        "--category-id",
        category_id,
        "--results",
        str(results_path),
    ]
    print("RUN", book_id)
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(f"FAIL {book_id}: exit {proc.returncode}")
    print("OK", book_id)


def main() -> None:
    for book_id, category_id, bodies in BODIES:
        write_and_complete(book_id, category_id, bodies)
    print("ALL_DONE")


if __name__ == "__main__":
    main()
