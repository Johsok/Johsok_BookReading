# -*- coding: utf-8 -*-
"""Generate findbook results JSON for batch68 food-wellness books."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
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


def load_lines(name: str) -> list[str]:
    path = ROOT / "tools" / "_batch68_data" / f"{name}.txt"
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 150, (name, len(lines))
    return lines


def main() -> None:
    books = [
        {
            "id": "05_food_wellness-20260718-31",
            "categoryId": "05_food_wellness",
            "title": "主廚的療癒餐桌：118盤讓細胞開心的料理",
            "author": "羅勻吟",
            "file": "b31",
        },
        {
            "id": "05_food_wellness-20260718-32",
            "categoryId": "05_food_wellness",
            "title": "食材123!聰明煮好菜：只須1~3樣，用最少的主食材，煮出無需繁複備料的省時料理、美味翻倍的主廚級好料，從此輕鬆上菜!",
            "author": "楊勝凱 蔡萬利",
            "file": "b32",
        },
        {
            "id": "05_food_wellness-20260718-33",
            "categoryId": "05_food_wellness",
            "title": "Superfood!地瓜不簡單：料理點心七十二變，國民美食好吃good!",
            "author": "拓蔬人料理團隊（施建瑋、蔡長志、曾秀微）",
            "file": "b33",
        },
        {
            "id": "05_food_wellness-20260718-34",
            "categoryId": "05_food_wellness",
            "title": "冷菜料理：汆燙、涼拌、冰鎮63道清爽夏日料理【附贈真冰涼~書籤小卡2張，用最簡單的步驟做最好吃料理】",
            "author": "蓮池陽子 連雪雅",
            "file": "b34",
        },
        {
            "id": "05_food_wellness-20260718-35",
            "categoryId": "05_food_wellness",
            "title": "「名店秘製調味料&料理」：跨越法義日中，專業Chef傳授獨家的風味關鍵，帶你深入瞭解星級餐廳色香味的176種秘訣與技巧",
            "author": "加藤順一 國居 優 岩坪 滋 田村亮介 野田雄紀 音羽 元",
            "file": "b35",
        },
    ]
    ok, fail = [], []
    for book in books:
        try:
            lines = load_lines(book["file"])
            path = write_results(book["id"], lines, book["title"], book["author"])
            run_writer(book["categoryId"], path)
            ok.append(book["id"])
            print("OK", book["id"])
        except Exception as exc:
            fail.append((book["id"], str(exc)))
            print("FAIL", book["id"], exc)
    print("SUCCESS", ok)
    print("FAILURES", fail)
    if fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
