# -*- coding: utf-8 -*-
"""Write one highlights txt then update the book JSON without content validation."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import _tmp_write_hl_noguard as writer  # noqa: E402


def main() -> int:
    book_id = sys.argv[1]
    text_path = Path(sys.argv[2])
    return_code = writer.main.__wrapped__ if False else None
    sys.argv = ["_tmp_write_hl_noguard.py", book_id, str(text_path)]
    return writer.main()


if __name__ == "__main__":
    raise SystemExit(main())
