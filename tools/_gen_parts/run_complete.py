# -*- coding: utf-8 -*-
"""Validate, write results JSON, and complete books 123-126."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402

PARTS = Path(__file__).resolve().parent

BOOKS = [
    (
        "01_business_startup-20260716-123",
        "勇往值錢",
        "于振源",
        "123.json",
    ),
    (
        "01_business_startup-20260716-124",
        "奈特論風險、不確定性與利潤：在不可預測世界中，判斷如何成為利潤來源",
        "法蘭克．奈特",
        "124.json",
    ),
    (
        "01_business_startup-20260716-125",
        "節省工時的100種方法：我在巴克萊銀行、AIG、安聯等外商主管身邊學會，品質與速度兼顧的時短工作術，不用拚命就有高績效。",
        "森田幸",
        "125.json",
    ),
    (
        "01_business_startup-20260716-126",
        "循環在有無之間：永豐一百年的永續智慧",
        "何壽川",
        "126.json",
    ),
]


def main() -> int:
    for book_id, title, author, filename in BOOKS:
        bodies = json.loads((PARTS / filename).read_text(encoding="utf-8"))
        highlights = [f"{i:03d}、{body.strip()}" for i, body in enumerate(bodies, 1)]
        validate_highlights(book_id, highlights, title, author)
        results_path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
        results_path.write_text(
            json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "findbook_writer.py"),
                "complete",
                "--category-id",
                "01_business_startup",
                "--results",
                str(results_path),
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if proc.stdout.strip():
            print(proc.stdout.strip())
        if proc.returncode != 0:
            print(proc.stderr, file=sys.stderr)
            return proc.returncode
        book = json.loads(
            (ROOT / "Books" / "01_business_startup" / f"{book_id}.json").read_text(
                encoding="utf-8-sig"
            )
        )
        assert book.get("highlightsSource") == "grok"
        assert book.get("chatgptStatus") == "complete"
        assert len(book.get("chatgptHighlights", [])) == 150
        print(f"written/{book_id}/150/grok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
