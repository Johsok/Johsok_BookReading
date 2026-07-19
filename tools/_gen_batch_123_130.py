# -*- coding: utf-8 -*-
"""Generate and complete grok highlights for books 123-130."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402


def load_bodies_module(path: Path) -> dict[str, list[str]]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.BOOKS


def pack(bodies: list[str]) -> list[str]:
    if len(bodies) != 150:
        raise ValueError(f"need 150, got {len(bodies)}")
    return [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]


def main() -> int:
    tools = ROOT / "tools"
    books: dict[str, list[str]] = {}
    for name in (
        "_bodies_123.py",
        "_bodies_124.py",
        "_bodies_125.py",
        "_bodies_126.py",
        "_bodies_127.py",
        "_bodies_128.py",
        "_bodies_129.py",
        "_bodies_130.py",
    ):
        books.update(load_bodies_module(tools / name))

    written = []
    for book_id, bodies in books.items():
        highlights = pack(bodies)
        book_path = ROOT / "Books" / "01_business_startup" / f"{book_id}.json"
        book = json.loads(book_path.read_text(encoding="utf-8-sig"))
        validate_highlights(book_id, highlights, book.get("title", ""), book.get("author", ""))
        out = tools / f".findbook_results_grok_{book_id}.json"
        out.write_text(
            json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        proc = subprocess.run(
            [
                sys.executable,
                str(tools / "findbook_writer.py"),
                "complete",
                "--category-id",
                "01_business_startup",
                "--results",
                str(out),
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        sys.stdout.write(proc.stdout)
        if proc.returncode != 0:
            sys.stderr.write(proc.stderr)
            return proc.returncode
        written.append(book_id)
        print(f"status\t{book_id}\twritten")
    print(f"TOTAL written={len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
