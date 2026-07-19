# -*- coding: utf-8 -*-
"""Generate and write findbook results for batch47 healthcare books."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from _batch47_bodies import H21, H22, H23, H24, H25  # noqa: E402

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


def write_and_run(book_id: str, category_id: str, lines: list[str], title: str, author: str) -> None:
    highlights = numbered(lines)
    validate_local(book_id, highlights, title, author)
    path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    path.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "findbook_writer.py"),
        "complete",
        "--category-id",
        category_id,
        "--results",
        str(path),
    ]
    print("RUN", book_id)
    subprocess.run(cmd, cwd=str(ROOT), check=True)


BOOKS = [
    (
        "04_healthcare-20260718-21",
        "04_healthcare",
        H21,
        "韓濟生的無創針灸新技術，經皮穴位電刺激療法：疼痛控制×睡眠管理×神經精神照護×內分泌調節，以無創電刺激延伸傳統針灸，涵蓋多種疾病照護與管理",
        "韓濟生 主編",
    ),
    (
        "04_healthcare-20260718-22",
        "04_healthcare",
        H22,
        "老祖宗傳下來不生病的智慧：融合《黃帝內經》、《本草綱目》等中醫經典，現代醫學驗證，藥補不如食補，打造強健、不生病的體質。",
        "張燦（編著者）",
    ),
    (
        "04_healthcare-20260718-23",
        "04_healthcare",
        H23,
        "圖解顏面診治",
        "李家雄",
    ),
    (
        "04_healthcare-20260718-24",
        "04_healthcare",
        H24,
        "偉大的迷走神經：人體內建的修復迴路，改善發炎、免疫與情緒的關鍵",
        "凱文‧特雷西 醫師",
    ),
    (
        "04_healthcare-20260718-25",
        "04_healthcare",
        H25,
        "爸媽最安心的嬰幼兒副食品【全新增訂版】─專業營養師教你養出不挑食的健康寶寶",
        "宋明樺．林俐岑 營養師",
    ),
]


def main() -> None:
    ok = []
    fail = []
    for book_id, category_id, lines, title, author in BOOKS:
        try:
            write_and_run(book_id, category_id, lines, title, author)
            ok.append(book_id)
        except Exception as exc:  # noqa: BLE001
            fail.append((book_id, str(exc)))
            print("FAIL", book_id, exc)
    print("OK", ok)
    print("FAIL", fail)
    if fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
