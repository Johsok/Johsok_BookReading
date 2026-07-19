# -*- coding: utf-8 -*-
"""Fix short-colon label lines in batch4 result JSON files."""
from __future__ import annotations

import json
import re
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
NUMBER_RE = re.compile(r"^\d{3}、")


def is_short_colon(body: str) -> bool:
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    return bool(match and not match.group(1).endswith(NATURAL))


def fix_body(body: str) -> str:
    """Rewrite short-label colon openings into natural sentences."""
    match = re.match(r"^([^：:]{1,12})[：:](.*)$", body)
    if not match:
        return body
    label, rest = match.group(1).strip(), match.group(2).strip()
    if label.endswith(NATURAL):
        return body
    # Prefer embedding label into a clause without short-label pattern.
    if rest:
        return f"關於{label}，{rest}"
    return body


def fix_file(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    highlights = data["highlights"]
    fixed = 0
    new_lines = []
    for line in highlights:
        body = NUMBER_RE.sub("", line, count=1).strip()
        if is_short_colon(body):
            body2 = fix_body(body)
            # If still short-colon (關於X still might be ok since 關於+label may exceed or use comma)
            if is_short_colon(body2):
                # Force: drop colon structure entirely
                m = re.match(r"^([^：:]{1,12})[：:](.*)$", body)
                label, rest = m.group(1).strip(), m.group(2).strip()
                body2 = f"{label}方面可以這樣理解，{rest}"
            prefix = line[:4]  # NNN、
            line = prefix + body2
            fixed += 1
        new_lines.append(line)
    data["highlights"] = new_lines
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return fixed


def main() -> None:
    ids = [
        "02_psychology_growth-20260718-21",
        "02_psychology_growth-20260718-22",
        "02_psychology_growth-20260718-23",
        "02_psychology_growth-20260718-24",
        "02_psychology_growth-20260718-25",
    ]
    for book_id in ids:
        path = TOOLS / f".findbook_results_grok_{book_id}.json"
        n = fix_file(path)
        # verify
        data = json.loads(path.read_text(encoding="utf-8"))
        bad = []
        for i, line in enumerate(data["highlights"], 1):
            body = NUMBER_RE.sub("", line, count=1).strip()
            if is_short_colon(body):
                bad.append((i, body[:40]))
        print(f"{book_id}: fixed={n}, remaining_bad={len(bad)}")
        for item in bad[:5]:
            print(" ", item)


if __name__ == "__main__":
    main()
