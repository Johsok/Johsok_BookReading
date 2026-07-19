# -*- coding: utf-8 -*-
"""Generate results JSON and run findbook_writer for batch57."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from _batch57_b26 import BOOK26  # noqa: E402
from _batch57_b27 import BOOK27  # noqa: E402
from _batch57_b28 import BOOK28  # noqa: E402
from _batch57_b29 import BOOK29  # noqa: E402
from _batch57_b30 import BOOK30  # noqa: E402

NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")

BOOKS = [
    {
        "id": "04_healthcare-20260718-26",
        "categoryId": "04_healthcare",
        "title": "日落之那邊：通路導向的癌症精準治療與康復新思維",
        "author": "翁一鳴",
        "lines": BOOK26,
    },
    {
        "id": "04_healthcare-20260718-27",
        "categoryId": "04_healthcare",
        "title": "元氣滿滿!漫畫養生小日常",
        "author": "石韋 著",
        "lines": BOOK27,
    },
    {
        "id": "04_healthcare-20260718-28",
        "categoryId": "04_healthcare",
        "title": "《金匱要略》內科臨床學：從教室走向臨床之路",
        "author": "張永明",
        "lines": BOOK28,
    },
    {
        "id": "04_healthcare-20260718-29",
        "categoryId": "04_healthcare",
        "title": "內在時鐘：從癌症到憂鬱症，從學童困境到工殤意外，生理時鐘失調的最新研究與改善之道",
        "author": "琳恩．皮普爾斯",
        "lines": BOOK29,
    },
    {
        "id": "04_healthcare-20260718-30",
        "categoryId": "04_healthcare",
        "title": "一按就通!圖解經絡按摩全書：按對穴位，百病自癒",
        "author": "謝文英",
        "lines": BOOK30,
    },
]


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


def main() -> None:
    ok = []
    fail = []
    for book in BOOKS:
        book_id = book["id"]
        try:
            path = write_results(book_id, book["lines"], book["title"], book["author"])
            run_writer(book["categoryId"], path)
            ok.append(book_id)
        except Exception as exc:  # noqa: BLE001
            fail.append((book_id, str(exc)))
            print(f"FAIL\t{book_id}\t{exc}")
    print("OK", ok)
    print("FAIL", fail)


if __name__ == "__main__":
    main()
