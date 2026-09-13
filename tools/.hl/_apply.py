# -*- coding: utf-8 -*-
"""Apply isolated Grok highlight text files to reserved books."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_highlights import write_highlights  # noqa: E402


def load_lines(path: Path) -> list[str]:
    found: dict[int, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip().replace("<|eos|>", "").strip()
        if len(line) >= 5 and line[3] == "、" and line[:3].isdigit():
            found[int(line[:3])] = line
    return [found[index] for index in range(1, 151) if index in found]


def main() -> int:
    folder = Path(__file__).resolve().parent
    targets = sys.argv[1:] or [path.stem for path in sorted(folder.glob("*.txt"))]
    for book_id in targets:
        path = folder / f"{book_id}.txt"
        lines = load_lines(path)
        if len(lines) != 150:
            raise SystemExit(f"{book_id} has {len(lines)} lines")
        print(write_highlights(ROOT, book_id, lines), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
