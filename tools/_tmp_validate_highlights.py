# -*- coding: utf-8 -*-
"""Local highlight validator mirroring findbook_writer.complete checks."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402


def dump_and_check(book_id: str, title: str, author: str, bodies: list[str]) -> None:
    if len(bodies) != 150:
        raise SystemExit(f"{book_id} count={len(bodies)}")
    highlights = [f"{i:03d}、{body}" for i, body in enumerate(bodies, 1)]
    validate_highlights(book_id, highlights, title, author)
    out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    payload = {"id": book_id, "highlights": highlights}
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ok\t{book_id}\t{out.name}")


if __name__ == "__main__":
    print("helper ready")
