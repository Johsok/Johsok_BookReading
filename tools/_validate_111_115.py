# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import NATURAL_COLON_SUFFIXES, read_json, validate_highlights

IDS = [
    "02_psychology_growth-20260717-111",
    "02_psychology_growth-20260717-112",
    "02_psychology_growth-20260717-113",
    "02_psychology_growth-20260717-114",
    "02_psychology_growth-20260717-115",
]
OUT = ROOT / "tools" / "_validate_111_115_out.txt"


def main() -> int:
    lines_out = []
    failed = 0
    colon_re = re.compile(r"^([^：:]{1,12})[：:]")
    for bid in IDS:
        path = ROOT / "tools" / f".findbook_results_grok_{bid}.json"
        data = read_json(path)
        book = read_json(ROOT / "Books" / "02_psychology_growth" / f"{bid}.json")
        try:
            validate_highlights(
                bid,
                data["highlights"],
                book.get("title", ""),
                book.get("author", ""),
            )
            lines_out.append(f"OK writer {bid}")
        except Exception as exc:
            failed += 1
            lines_out.append(f"FAIL writer {bid}: {exc}")
        colon_hits = []
        latin_hits = []
        for index, line in enumerate(data["highlights"], 1):
            body = re.sub(r"^\d{3}、", "", line, count=1).strip()
            match = colon_re.match(body)
            if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
                colon_hits.append(f"  COLON #{index:03d} [{match.group(1)}] {body}")
            latin = re.findall(r"[A-Za-z]{2,}", body)
            if latin:
                latin_hits.append(f"  LATIN #{index:03d} {latin} {body}")
        lines_out.append(f"  colon_count={len(colon_hits)}")
        lines_out.extend(colon_hits)
        lines_out.extend(latin_hits)
        lines_out.append("")
    OUT.write_text("\n".join(lines_out), encoding="utf-8")
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
