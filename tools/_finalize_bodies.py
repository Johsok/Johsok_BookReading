# -*- coding: utf-8 -*-
"""Validate body txt, write result json, run complete."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402

META = {
    "04_healthcare-20260719-03": (
        "開啟身體自癒、逆齡瘦身、泌尿道照護套書(共2本)：自噬力：開啟身體自癒、逆齡與瘦身的科學飲食法+完全詳解 泌尿道診治照護全書",
        "洪泰雄,台灣泌尿科醫學會、王炯珵",
    ),
    "05_food_wellness-20260719-01": (
        "食材123！聰明煮好菜：只須1～3樣，用最少的主食材，煮出無需繁複備料的省時料理、美味翻倍的主廚級好料，從此輕鬆上菜！",
        "蔡萬利,楊勝凱",
    ),
    "05_food_wellness-20260719-02": (
        "「名店秘製調味料&料理」：跨越法義日中，專業Chef傳授獨家的風味關鍵，帶你深入瞭解星級餐廳色香味的176種秘訣與技巧",
        "岩坪 滋,音羽 元,加藤順一,野田雄紀,國居 優,田村亮介",
    ),
    "06_computer_info-20260719-01": (
        "人手一本的 Vibe Coding 資安實作課：不是專家也能自己動手與 AI 協作！從專案生成、攻防演練到資安框架一次學會！（OWASP Top 10 × ISO27001）",
        "陳瑞麟",
    ),
    "07_other-20260719-01": (
        "1916之後，群雄逐鹿的北洋政府：北洋政局、派系競逐、革命餘波、財政困境……當移植的社會新制度與現實衝突，晚清後的民國如何在混亂時局中轉型？",
        "趙焰",
    ),
    "07_other-20260719-02": (
        "南北朝裂土誌──北齊開國與江南兵劫：賀拔遇害、宇文接軍、孝武入關、高歡失玉璧、侯景破臺城……北方雙雄對峙未決，江南帝國為何先一步走向崩壞？",
        "譚自安",
    ),
}


def process(book_id: str) -> None:
    title, author = META[book_id]
    txt = ROOT / "tools" / f"_bodies_{book_id}.txt"
    lines = [ln.strip() for ln in txt.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if len(lines) != 150:
        raise SystemExit(f"{book_id} count={len(lines)}")
    highlights = [f"{i:03d}、{b}" for i, b in enumerate(lines, 1)]
    validate_highlights(book_id, highlights, title, author)
    out = ROOT / "tools" / f".findbook_result_{book_id}.json"
    out.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("wrote", out.name)
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "_complete_grok_20260719.py"), "--results", str(out)],
        cwd=str(ROOT),
    )
    if r.returncode != 0:
        raise SystemExit(f"complete failed {book_id} code={r.returncode}")


if __name__ == "__main__":
    ids = sys.argv[1:] or ["04_healthcare-20260719-03"]
    for book_id in ids:
        process(book_id)
