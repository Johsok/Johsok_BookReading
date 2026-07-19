# -*- coding: utf-8 -*-
"""Load batch77 highlight parts, assemble 150 each, write via findbook_writer."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")


def numbered(lines: list[str]) -> list[str]:
    assert len(lines) == 150, len(lines)
    return [f"{i:03d}、{b.strip()}" for i, b in enumerate(lines, 1)]


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


def write_and_run(book_id: str, category_id: str, lines: list[str], title: str, author: str) -> None:
    highlights = numbered(lines)
    validate_local(book_id, highlights, title, author)
    path = TOOLS / f".findbook_results_grok_{book_id}.json"
    path.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        str(TOOLS / "findbook_writer.py"),
        "complete",
        "--category-id",
        category_id,
        "--results",
        str(path),
    ]
    print("RUN", book_id)
    subprocess.run(cmd, cwd=str(ROOT), check=True)


def load_json(name: str):
    return json.loads((TOOLS / name).read_text(encoding="utf-8"))


def main() -> None:
    partial = load_json("_b77_partial.json")
    extras = load_json("_b77_extras.json")
    book36 = partial["BOOK36"] + extras["EXTRA36"]
    book37 = partial["BOOK37"] + extras["EXTRA37"]
    book38 = partial["BOOK38"] + load_json("_b77_extra38.json")
    book39 = load_json("_b77_book39.json")
    book40 = load_json("_b77_book40.json")

    books = [
        {
            "id": "04_healthcare-20260718-36",
            "categoryId": "04_healthcare",
            "title": "激素平衡瘦身課(限量附贈【14天代謝調整課表】)：啟動代謝重建，瘦得健康持久",
            "author": "許書華",
            "lines": book36,
        },
        {
            "id": "04_healthcare-20260718-37",
            "categoryId": "04_healthcare",
            "title": "看透醫學謊言，找到代謝真相：逆轉肥胖、高血壓、脂肪肝，讓身體健康長壽的自救指南",
            "author": "羅伯特．勒夫金 丁亦",
            "lines": book37,
        },
        {
            "id": "04_healthcare-20260718-38",
            "categoryId": "04_healthcare",
            "title": "輕鬆當爸媽，孩子更健康【最新增修版】：超人氣小兒科醫師黃瑽寧教你安心育兒",
            "author": "黃瑽寧",
            "lines": book38,
        },
        {
            "id": "04_healthcare-20260718-39",
            "categoryId": "04_healthcare",
            "title": "讀懂身體的訊號：基因醫師教你逆轉健康危機",
            "author": "張家銘",
            "lines": book39,
        },
        {
            "id": "04_healthcare-20260718-40",
            "categoryId": "04_healthcare",
            "title": "科學實證有效的休息100招攻略：用最短時間快速提升專注力、恢復體力和身心健康",
            "author": "加藤浩晃 陳欣如",
            "lines": book40,
        },
    ]

    written = []
    failures = []
    for book in books:
        try:
            assert len(book["lines"]) == 150, (book["id"], len(book["lines"]))
            write_and_run(
                book["id"],
                book["categoryId"],
                book["lines"],
                book["title"],
                book["author"],
            )
            written.append(book["id"])
        except Exception as exc:  # noqa: BLE001
            failures.append((book["id"], str(exc)))
            print("FAIL", book["id"], exc)
    print("SUCCESS", written)
    print("FAILURE", failures)
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
