# -*- coding: utf-8 -*-
"""Fix short-colon highlight lines and re-run findbook_writer."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")


def is_short_colon(body: str) -> bool:
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    return bool(match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES))


def fix_body(body: str) -> str:
    """Rewrite short-label colons into natural prose."""
    match = re.match(r"^([^：:]{1,12})[：:](.+)$", body)
    if not match:
        return body
    left, right = match.group(1).strip(), match.group(2).strip()
    if left.endswith(NATURAL_COLON_SUFFIXES):
        return body
    # Prefer comma splice; keep meaning.
    if right.startswith(("例如", "包括", "像是", "亦即")):
        return f"{left}，{right}"
    return f"{left}，指的是{right}" if len(left) <= 6 else f"{left}，{right}"


def process(book_id: str, category_id: str) -> None:
    path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    highlights = data["highlights"]
    fixed = []
    changes = 0
    for i, line in enumerate(highlights, 1):
        expected = f"{i:03d}、"
        body = line[len(expected) :]
        if is_short_colon(body):
            new_body = fix_body(body)
            if new_body != body:
                changes += 1
                line = expected + new_body
                print(f"{book_id} #{i}: {body[:40]} -> {new_body[:40]}")
        fixed.append(line)
    # Ensure fewer than 3 short-colon remain; force-fix any leftovers.
    leftover = []
    final = []
    for i, line in enumerate(fixed, 1):
        expected = f"{i:03d}、"
        body = line[len(expected) :]
        if is_short_colon(body):
            body2 = body.replace("：", "，", 1).replace(":", "，", 1)
            line = expected + body2
            leftover.append(i)
            changes += 1
        final.append(line)
    data["highlights"] = final
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{book_id}: changed={changes}, leftover_forced={leftover}")

    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "findbook_writer.py"),
            "complete",
            "--category-id",
            category_id,
            "--results",
            str(path),
        ],
        cwd=str(ROOT),
        capture_output=True,
    )
    out = (proc.stdout or b"").decode("utf-8", errors="replace")
    err = (proc.stderr or b"").decode("utf-8", errors="replace")
    if proc.returncode != 0:
        print(f"FAIL {book_id}: {err or out}")
        raise SystemExit(proc.returncode)
    print(f"OK {book_id}: {out.strip()}")


def main() -> int:
    for book_id in [
        "04_healthcare-20260718-06",
        "04_healthcare-20260718-08",
        "04_healthcare-20260718-09",
        "04_healthcare-20260718-10",
    ]:
        process(book_id, "04_healthcare")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
