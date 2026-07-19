# -*- coding: utf-8 -*-
"""Generate grok highlights for five 20260718 books and run findbook_writer."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent

NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
FORBIDDEN = ("本書", "作者指出", "本章", "這一章")


def fmt(items: list[str]) -> list[str]:
    if len(items) != 150:
        raise SystemExit(f"need 150 got {len(items)}")
    out = []
    for i, body in enumerate(items, 1):
        body = body.strip()
        if re.match(r"^\d{3}、", body):
            body = body[4:].strip()
        out.append(f"{i:03d}、{body}")
    return out


def local_validate(book_id: str, highlights: list[str], title: str = "", author: str = "") -> None:
    if len(highlights) != 150:
        raise ValueError(f"{book_id} count {len(highlights)}")
    short_colon = []
    bodies = []
    for index, line in enumerate(highlights, 1):
        expected = f"{index:03d}、"
        if not line.startswith(expected):
            raise ValueError(f"{book_id} #{index} numbering")
        if "\n" in line or "\r" in line or "｜" in line:
            raise ValueError(f"{book_id} #{index} bad format")
        body = NUMBER_RE.sub("", line, count=1).strip()
        if len(body) < 12:
            raise ValueError(f"{book_id} #{index} too short: {body}")
        if any(p in body for p in FORBIDDEN):
            raise ValueError(f"{book_id} #{index} forbidden")
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            raise ValueError(f"{book_id} #{index} step wording")
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(NATURAL_COLON_SUFFIXES):
            short_colon.append(index)
        bodies.append(body)
    if len(short_colon) >= 3:
        raise ValueError(f"{book_id} short colon labels: {short_colon[:10]}")
    if len(set(bodies)) != len(bodies):
        c = Counter(bodies)
        dups = [b for b, n in c.items() if n > 1]
        raise ValueError(f"{book_id} exact dups: {dups[:3]}")
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    top = starts.most_common(1)[0]
    if top[1] >= 4:
        raise ValueError(f"{book_id} repeated starts ({top[1]}): {top[0]!r}")
    for label, value in (("title", title), ("author", author)):
        if value and sum(value in b for b in bodies) >= 2:
            raise ValueError(f"{book_id} repeats full {label}")


BOOKS: dict[str, tuple[str, str, list[str]]] = {}

# populated below via exec of data sections
exec(open(TOOLS / "_gen_highlights_data0718.py", encoding="utf-8").read(), globals())


def main() -> int:
    for book_id, (title, author, raw) in BOOKS.items():
        highlights = fmt(raw)
        local_validate(book_id, highlights, title, author)
        results_path = TOOLS / f".findbook_results_grok_{book_id}.json"
        payload = {"id": book_id, "highlights": highlights, "source": "grok"}
        results_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"results\t{book_id}\t{results_path}")
        cmd = [
            sys.executable,
            str(TOOLS / "findbook_writer.py"),
            "--root",
            str(ROOT),
            "complete",
            "--results",
            str(results_path),
        ]
        proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        if proc.returncode != 0:
            raise SystemExit(proc.returncode)
        book_path = ROOT / "Books" / "01_business_startup" / f"{book_id}.json"
        saved = json.loads(book_path.read_text(encoding="utf-8-sig"))
        assert len(saved["chatgptHighlights"]) == 150
        assert saved["chatgptStatus"] == "complete"
        assert saved["highlightsSource"] == "grok"
        print(
            f"verified\t{book_id}\tcount={len(saved['chatgptHighlights'])}"
            f"\tstatus={saved['chatgptStatus']}\tsource={saved['highlightsSource']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
