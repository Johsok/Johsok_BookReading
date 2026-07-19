# -*- coding: utf-8 -*-
"""Pack bodies into result JSON and optionally complete."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402


def load_books(path: Path) -> dict:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod.BOOKS


def pack_from_module(path: Path, book_ids: list[str] | None = None) -> None:
    books = load_books(path)
    for book_id, (title, author, bodies) in books.items():
        if book_ids and book_id not in book_ids:
            continue
        if len(bodies) != 150:
            raise SystemExit(f"{book_id} count={len(bodies)}")
        highlights = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
        validate_highlights(book_id, highlights, title, author)
        out = ROOT / "tools" / f".findbook_result_{book_id}.json"
        out.write_text(
            json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )
        print(f"wrote {out.name}")


def pack_from_txt(book_id: str, title: str, author: str, txt_path: Path) -> None:
    lines = [ln.strip() for ln in txt_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if len(lines) != 150:
        raise SystemExit(f"{book_id} txt count={len(lines)}")
    highlights = [f"{i:03d}、{b}" for i, b in enumerate(lines, 1)]
    validate_highlights(book_id, highlights, title, author)
    out = ROOT / "tools" / f".findbook_result_{book_id}.json"
    out.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out.name}")


if __name__ == "__main__":
    pack_from_module(ROOT / "tools" / "_gen_grok_20260719_hl_p1.py")
