# -*- coding: utf-8 -*-
"""Extra QA for the two highlight JSON files."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
FORBIDDEN = ("本書", "作者指出", "本章", "這一章", "｜")
CHAPTER_RE = re.compile(r"第[一二三四五六七八九十百零0-9]+章")
SIMP_CHARS = set("为这从对会开时样经现点体国医后说让还过发种长东见应该么复处实据护击虽仅")


def qa(path: Path, title: str, author: str) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert set(data.keys()) == {"id", "highlights"}, data.keys()
    hs = data["highlights"]
    assert len(hs) == 150, len(hs)
    bodies = []
    for i, line in enumerate(hs, 1):
        assert line.startswith(f"{i:03d}、"), line[:10]
        assert "\n" not in line and "\r" not in line
        body = line.split("、", 1)[1]
        assert len(body) >= 12, (i, body)
        for bad in FORBIDDEN:
            assert bad not in body, (i, bad)
        assert not CHAPTER_RE.search(body), (i, body)
        hit = [c for c in body if c in SIMP_CHARS]
        assert not hit, (i, hit, body)
        bodies.append(body)
    assert len(set(bodies)) == 150
    starts = Counter(b[:18] for b in bodies)
    top = starts.most_common(1)[0]
    assert top[1] < 4, top
    assert sum(title in b for b in bodies) <= 1
    assert sum(author in b for b in bodies) <= 1
    print(path.name, "OK 150/150", "top_prefix", top)


qa(
    OUT / "03_natural_science-20260709-05.json",
    "腸腦悖論：揭開腸道如何左右你的情緒、記憶與行為",
    "史蒂芬．R．岡德里",
)
qa(
    OUT / "03_natural_science-20260709-06.json",
    "找樹的人2：台灣巨木地圖全紀錄（震撼全台紀錄片《神木之島》故事源頭∕徐嘉君第一手紀錄）",
    "徐嘉君",
)
print("official books untouched check skipped here")
