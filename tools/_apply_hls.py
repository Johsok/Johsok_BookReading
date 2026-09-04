# -*- coding: utf-8 -*-
"""Apply numbered highlight lines to reserved book JSON via write_highlights."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_highlights import extract_highlights, write_highlights


def has_garbled(text: str) -> bool:
    """Return True when replacement chars or typical mojibake appear."""
    if "\ufffd" in text or "锟斤拷" in text or "ï¿½" in text:
        return True
    if "Ã" in text and any("\u4e00" <= ch <= "\u9fff" for ch in text):
        return True
    return False


def apply_batch(path: Path) -> None:
    """Split ===BOOK=== sections and write each 150-line book."""
    raw = path.read_text(encoding="utf-8")
    if has_garbled(raw):
        raise SystemExit(f"garbled text in {path}")
    parts = raw.split("===BOOK===")
    root = Path(__file__).resolve().parents[1]
    for part in parts:
        part = part.strip()
        if not part:
            continue
        first, _, rest = part.partition("\n")
        book_id = first.strip()
        lines = extract_highlights(rest)
        if len(lines) != 150:
            raise SystemExit(f"{book_id} extracted {len(lines)} lines")
        if any(has_garbled(line) for line in lines):
            raise SystemExit(f"{book_id} garbled highlight line")
        result = write_highlights(root, book_id, lines)
        print(f"written {result['id']} count={result['count']}")


if __name__ == "__main__":
    apply_batch(Path(sys.argv[1]).resolve())
