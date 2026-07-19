# -*- coding: utf-8 -*-
"""Generate findbook results JSON for batch50 other-category books."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from importlib.machinery import SourceFileLoader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")


def numbered(lines: list[str]) -> list[str]:
    assert len(lines) == 150, len(lines)
    out = []
    for i, body in enumerate(lines, 1):
        body = body.strip()
        assert len(body) >= 12, (i, body)
        out.append(f"{i:03d}、{body}")
    return out


def validate_local(book_id: str, highlights: list[str], title: str = "", author: str = "") -> None:
    short_colon = []
    bodies = []
    forbidden = ("本書", "作者指出", "本章", "這一章")
    for index, line in enumerate(highlights, 1):
        expected = f"{index:03d}、"
        assert line.startswith(expected), (book_id, index, line[:40])
        assert "\n" not in line and "\r" not in line and "｜" not in line
        body = NUMBER_RE.sub("", line, count=1).strip()
        assert len(body) >= 12, (book_id, index, body)
        for p in forbidden:
            assert p not in body, (book_id, index, p)
        assert not re.search(r".{1,8}面第\d+步[，,]", body)
        assert not re.match(r"^第\d+步[，,]", body)
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(NATURAL_COLON_SUFFIXES):
            short_colon.append(index)
        bodies.append(body)
    assert len(short_colon) < 3, (book_id, short_colon)
    assert len(set(bodies)) == 150, book_id
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    assert starts.most_common(1)[0][1] < 4, (book_id, starts.most_common(3))
    for label, value in (("title", title), ("author", author)):
        if value and sum(value in b for b in bodies) >= 2:
            raise AssertionError(f"{book_id} repeats {label}")


def write_results(book_id: str, lines: list[str], title: str = "", author: str = "") -> Path:
    highlights = numbered(lines)
    validate_local(book_id, highlights, title, author)
    path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    path.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def run_writer(category_id: str, results_path: Path) -> None:
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "findbook_writer.py"),
        "complete",
        "--category-id",
        category_id,
        "--results",
        str(results_path),
    ]
    print("RUN", " ".join(cmd))
    subprocess.run(cmd, cwd=str(ROOT), check=True)


def _load(module_path: str, attr: str) -> list[str]:
    mod = SourceFileLoader(attr, str(ROOT / "tools" / module_path)).load_module()
    return getattr(mod, attr)


def main() -> None:
    batch = [
        {
            "id": "07_other-20260718-21",
            "categoryId": "07_other",
            "title": "盛世之鑰：為何開放的社會更強大?從七個黃金時代看文明興衰的真相",
            "author": "約翰．諾貝里",
            "lines": _load("_batch50_b21.py", "BOOK21"),
        },
        {
            "id": "07_other-20260718-22",
            "categoryId": "07_other",
            "title": "追夢者的美國歷程：18個大時代中的移民故事",
            "author": "林志濤,黃莉翔",
            "lines": _load("_batch50_b22.py", "BOOK22"),
        },
        {
            "id": "07_other-20260718-23",
            "categoryId": "07_other",
            "title": "詐騙的14種信號：與詐欺師交手的實戰經驗祕笈，教你避開騙術陷阱",
            "author": "強納森．沃爾頓Johnathan Walton",
            "lines": _load("_batch50_b23.py", "BOOK23"),
        },
        {
            "id": "07_other-20260718-24",
            "categoryId": "07_other",
            "title": "普通人不會扛起機關槍：一位父親、丈夫、前和平主義者對戰爭的思考",
            "author": "阿爾特姆．查派",
            "lines": _load("_batch50_b24.py", "BOOK24"),
        },
        {
            "id": "07_other-20260718-25",
            "categoryId": "07_other",
            "title": "花香園的女兒們：被海峽分隔的兩姊妹",
            "author": "李竹青",
            "lines": _load("_batch50_b25.py", "BOOK25"),
        },
    ]
    ok = []
    failed = []
    for book in batch:
        try:
            path = write_results(book["id"], book["lines"], book["title"], book["author"])
            run_writer(book["categoryId"], path)
            ok.append(book["id"])
            print("OK", book["id"])
        except Exception as exc:
            failed.append((book["id"], str(exc)))
            print("FAIL", book["id"], exc)
    print("SUCCESS", ok)
    print("FAILED", failed)


if __name__ == "__main__":
    main()
