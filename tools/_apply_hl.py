# -*- coding: utf-8 -*-
"""Apply tools/.hl_{book_id}.txt into the corresponding book JSON."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from findbook_highlights import write_highlights  # noqa: E402


def main() -> int:
    targets = sys.argv[1:]
    paths = (
        [TOOLS / f".hl_{book_id}.txt" for book_id in targets]
        if targets
        else sorted(TOOLS.glob(".hl_*.txt"))
    )
    failed = 0
    for path in paths:
        book_id = path.name[4:-4]
        if not path.exists():
            print(f"MISS\t{book_id}")
            failed += 1
            continue
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        try:
            result = write_highlights(ROOT, book_id, lines)
            print(f"OK\t{result['id']}\t{result['count']}")
        except Exception as exc:
            print(f"FAIL\t{book_id}\t{exc}")
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
