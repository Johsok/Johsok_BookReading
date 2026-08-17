# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


def validate_and_write(book_id: str, title: str, author: str, bodies: list[str]) -> None:
    assert len(bodies) == 150, len(bodies)
    natural = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
    highlights = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
    forb = [
        "落到具體情境，再用可觀察的結果確認做法是否有效",
        "作為判斷線索時",
        "先界定目標，再把",
        "先盤點條件，再把",
        "本書",
        "作者指出",
        "本章",
        "這一章",
        "｜",
    ]
    text = "\n".join(highlights)
    for f in forb:
        assert f not in text, f
    sc = []
    for i, b in enumerate(bodies, 1):
        assert len(b) >= 12, (i, b)
        if re.search(r".{1,8}面第\d+步[，,]", b) or re.match(r"^第\d+步[，,]", b):
            raise AssertionError(f"step {i}")
        m = re.match(r"^([^：:]{1,12})[：:]", b)
        if m and not m.group(1).endswith(natural):
            sc.append((i, b[:50]))
    assert len(set(bodies)) == 150
    c = Counter(b[:18] for b in bodies)
    assert c.most_common(1)[0][1] < 4, c.most_common(5)
    assert sum(title in b for b in bodies) < 2
    assert sum(author in b for b in bodies) < 2
    assert len(sc) < 3, sc
    out = Path(__file__).with_name(f".findbook_results_grok_{book_id}.json")
    out.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("ok", book_id)


def load_bodies_from_gen12() -> list[str]:
    raw = Path(__file__).with_name("_gen_12.py").read_text(encoding="utf-8-sig")
    start = raw.index("BODIES = [")
    end = raw.index("\n]\n", start)
    chunk = raw[start + len("BODIES = [") : end]
    bodies = []
    for line in chunk.splitlines():
        line = line.strip().rstrip(",")
        if line.startswith('"') and line.endswith('"'):
            bodies.append(line[1:-1])
    bodies = [b.replace(" thrush 消失", "推舌反射減弱") for b in bodies]
    # drop the last if 151
    if len(bodies) > 150:
        bodies = bodies[:150]
    return bodies


if __name__ == "__main__":
    bodies = load_bodies_from_gen12()
    validate_and_write(
        "02_psychology_growth-20260724-12",
        "超高效正向育兒 搞定睡眠 調整作息 100道副食品套書(共2本)：鈞媽快樂育兒經+營養師&兒科醫師副食品配方",
        "鈞媽,湯國廷,廖嘉音",
        bodies,
    )
