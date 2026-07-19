# -*- coding: utf-8 -*-
"""Generate and write findbook highlights for batch78."""
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
CATEGORY = "05_food_wellness"


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


def run_writer(results_path: Path) -> None:
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "findbook_writer.py"),
        "complete",
        "--category-id",
        CATEGORY,
        "--results",
        str(results_path),
    ]
    print("RUN", " ".join(cmd))
    subprocess.run(cmd, cwd=str(ROOT), check=True)


def load_lines(name: str) -> list[str]:
    path = ROOT / "tools" / "_batch78_highlights" / f"{name}.txt"
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 150, (name, len(lines))
    return lines


def main() -> None:
    books = [
        ("05_food_wellness-20260718-36", "b36", "1次煮5天便當：營養師親自設計健康又美味的料理", "阿杉(Osugi) 黃詩婷"),
        ("05_food_wellness-20260718-37", "b37", "肉の料理科學超圖解【暢銷修訂版】 ：大廚不外傳的雞豬牛羊306個部位烹調密技，從選對肉到出好菜一本搞定!", "朝日新聞出版 鄭睿芝"),
        ("05_food_wellness-20260718-38", "b38", "高代謝地中海日常菜：早午餐X便當菜X常備菜，「全球最佳飲食法」75道減醣低卡速簡料理", "謝長鴻（馬可）"),
        ("05_food_wellness-20260718-39", "b39", "貝姬的韓式瘦身微波爐食譜：狂瘦35公斤!100道低熱量、高蛋白、高膳食纖維料理", "貝姬（金炫京） 林季妤"),
        ("05_food_wellness-20260718-40", "b40", "今天煮什麼?：型男主廚吳秉承的百搭美味方程式，活用15種食材╳6種鍋具小家電，教你又快又省錢，搞定一桌超營養料理!", "吳秉承"),
    ]
    ok, failed = [], []
    for book_id, key, title, author in books:
        try:
            lines = load_lines(key)
            path = write_results(book_id, lines, title, author)
            run_writer(path)
            ok.append(book_id)
        except Exception as exc:
            failed.append((book_id, str(exc)))
            print(f"FAIL {book_id}: {exc}")
    print("SUCCESS", ok)
    print("FAILED", failed)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
