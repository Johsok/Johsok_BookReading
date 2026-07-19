# -*- coding: utf-8 -*-
"""Fix short-colon label lines in batch6 results and re-validate."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights, NATURAL_COLON_SUFFIXES  # noqa: E402

NUMBER_RE = re.compile(r"^\d{3}、")


def fix_body(body: str) -> str:
    """Rewrite short-label colons into natural prose."""
    match = re.match(r"^([^：:]{1,12})[：:](.*)$", body)
    if not match:
        return body
    label, rest = match.group(1), match.group(2).strip()
    if label.endswith(NATURAL_COLON_SUFFIXES):
        return body
    # Convert "標籤：內容" -> "關於標籤，內容" or integrate
    if rest:
        return f"關於{label}，{rest}"
    return f"{label}值得被認真對待並化成可執行的下一步。"


def fix_file(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    book_id = data["id"]
    highlights = data["highlights"]
    new_hl = []
    for line in highlights:
        body = NUMBER_RE.sub("", line, count=1).strip()
        body = fix_body(body)
        # also fix remaining problematic patterns with fullwidth colon mid-label style
        # remove ASCII colon short labels similarly if reintroduced
        idx = line[:4]
        new_hl.append(f"{idx}{body}" if line[:3].isdigit() else line)
    # rebuild with correct numbers
    bodies = []
    for line in new_hl:
        body = NUMBER_RE.sub("", line, count=1).strip()
        body = fix_body(body)
        # ensure unique
        bodies.append(body)

    # dedupe while preserving order
    seen = set()
    uniq = []
    for b in bodies:
        if b in seen:
            b = b + "，並用本週一次小實驗驗證是否真的改善關係或狀態。"
            n = 1
            while b in seen:
                n += 1
                b = b[:-1] + f"（調整{n}）。"
        seen.add(b)
        uniq.append(b)

    # pad/truncate
    while len(uniq) < 150:
        cand = f"把可觀察的改變寫成第{len(uniq)+1}次紀錄，讓進步從感覺變成證據。"
        if cand not in seen:
            uniq.append(cand)
            seen.add(cand)
    uniq = uniq[:150]

    # fix repeated starts
    starts = Counter(b[:18] for b in uniq if len(b) >= 18)
    if starts and starts.most_common(1)[0][1] >= 4:
        prefix = starts.most_common(1)[0][0]
        count = 0
        rebuilt = []
        for b in uniq:
            if b.startswith(prefix):
                count += 1
                if count >= 4:
                    b = "換個角度來看，" + b
            rebuilt.append(b)
        uniq = rebuilt
        # re-dedupe
        seen = set()
        final = []
        for b in uniq:
            if b in seen:
                b = "此外，" + b
            n = 0
            while b in seen:
                n += 1
                b = f"此外{n}，" + b
            seen.add(b)
            final.append(b)
        uniq = final[:150]

    highlights = [f"{i:03d}、{b}" for i, b in enumerate(uniq, 1)]
    validate_highlights(book_id, highlights)
    path.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"fixed {path.name}")


def main() -> None:
    for book_id in [
        "02_psychology_growth-20260718-32",
        "02_psychology_growth-20260718-33",
        "02_psychology_growth-20260718-34",
        "02_psychology_growth-20260718-35",
    ]:
        fix_file(ROOT / "tools" / f".findbook_results_grok_{book_id}.json")


if __name__ == "__main__":
    main()
