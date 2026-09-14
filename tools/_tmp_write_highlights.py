# -*- coding: utf-8 -*-
"""Write one book's 150 highlights from a UTF-8 text file."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_highlights as h  # noqa: E402

book_id = sys.argv[1]
text_path = Path(sys.argv[2])
text = text_path.read_text(encoding="utf-8")
lines = h.extract_highlights(text)
print(book_id, "extracted", len(lines), flush=True)
if len(lines) != 150:
    raise SystemExit(f"{book_id} extracted {len(lines)}")
print(h.write_highlights(ROOT, book_id, lines), flush=True)
