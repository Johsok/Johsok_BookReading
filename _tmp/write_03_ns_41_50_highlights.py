# -*- coding: utf-8 -*-
"""Write 150 Traditional Chinese highlights for 03_natural_science-20260717-41..50."""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

REPO = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
ROOT = REPO / "Books" / "03_natural_science"
UPDATED = "2026-08-18"
CAPTURED = "2026-08-18T15:30:00+08:00"
BANNED = ("本書", "作者指出", "本章", "這一章", "｜")
COLON_RE = re.compile(r"[：:]")
STEP_RE = re.compile(r".面第\d+步")

sys.path.insert(0, str(REPO / "_tmp"))
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(ROOT))

from _gen_book41_42 import BOOK41, BOOK42  # noqa: E402
from _book43_44_highlights import BOOK43, BOOK44  # noqa: E402
from _gen_ns_45_46 import BOOK45, BOOK46  # noqa: E402
from _gen_47 import BOOK47, BOOK48  # noqa: E402
from _tmp_book49_50 import BOOK49, BOOK50  # noqa: E402

BOOKS: list[tuple[str, list[str], list[str], str]] = [
    (
        "03_natural_science-20260717-41.json",
        BOOK41,
        ["自然科學", "氣候變遷", "全球暖化", "兒童科普"],
        "韓國兒童科普「未來已來」氣候變遷分冊，用故事說明溫室氣體、冰層消退、極端氣候與減碳選項，並把個人行動接到系統改革。",
    ),
    (
        "03_natural_science-20260717-42.json",
        BOOK42,
        ["自然科學", "料理科學", "食物化學", "家庭實驗"],
        "以美乃滋乳化、蛋的凝固、乳品轉化、色素變色、果醬果膠、味覺交互與鹽的作用，把廚房操作寫成可重做的科學實驗。",
    ),
    (
        "03_natural_science-20260717-43.json",
        BOOK43,
        ["自然科學", "爬蟲飼養", "特寵醫療", "臨床案例"],
        "以臨床病例說明烏龜、蜥蜴、守宮、變色龍與蛇類的溫濕、UVB、鈣磷與常見急症，強調多數疾病源自飼養管理而非神秘傳染。",
    ),
    (
        "03_natural_science-20260717-44.json",
        BOOK44,
        ["自然科學", "漫畫科普", "冷知識", "生活科學"],
        "用漫畫把人體、動物、日常器物、科技與宇宙冷知識寫成可解釋的因果句，讓趣味trivia回到可驗證的科學機制。",
    ),
    (
        "03_natural_science-20260717-45.json",
        BOOK45,
        ["自然科學", "地球未來", "冰河週期", "太空移民", "兒童科普"],
        "從米蘭科維奇冰期、太陽演化、小行星風險談到適居帶行星與推進極限，區分當下人為暖化與萬年尺度的自然氣候擺盪。",
    ),
    (
        "03_natural_science-20260717-46.json",
        BOOK46,
        ["自然科學", "基本電學", "電工原理", "國營考試"],
        "依電荷、電阻、迴路、電容電感、暫態、交流阻抗、功率因數與諧振整理應試電學，把公式接到可計算的電路判斷。",
    ),
    (
        "03_natural_science-20260717-47.json",
        BOOK47,
        ["自然科學", "地動說", "天文學史", "知識與權力"],
        "以十五世紀壓迫下的地動說傳承，把托勒密本輪、逆行、自轉公轉與觀測紀錄，接到求知、懷疑與暴力之間的衝突。",
    ),
    (
        "03_natural_science-20260717-48.json",
        BOOK48,
        ["自然科學", "無人機", "人工智慧", "電腦視覺", "法規倫理"],
        "說明無人機構型、感測導航、機器學習與資安，以及農業監測、救災物流、智慧城市與空域法規的實務限制。",
    ),
    (
        "03_natural_science-20260717-49.json",
        BOOK49,
        ["自然科學", "材料科學", "石墨烯", "氣凝膠", "超材料", "兒童科普"],
        "從摺紙結構、陶瓷、石墨石墨烯、自癒混凝土、氣凝膠到生物材料與超材料，說明功能來自原子排列與微觀結構而非魔法名稱。",
    ),
    (
        "03_natural_science-20260717-50.json",
        BOOK50,
        ["自然科學", "化學", "碳同素異形體", "氣體", "溶液", "國中理化"],
        "以武俠漫畫包裝碳的結構、氫氦氧氮的活性差異，以及溶解、沉澱與乳化，對應國中理化常見物質變化。",
    ),
]


def validate(name: str, items: list[str], title: str = "", author: str = "") -> None:
    if len(items) != 150:
        raise SystemExit(f"{name}: expected 150, got {len(items)}")
    for i, text in enumerate(items, 1):
        for b in BANNED:
            if b in text:
                raise SystemExit(f"{name} #{i}: banned `{b}`")
        if COLON_RE.search(text):
            raise SystemExit(f"{name} #{i}: colon found")
        if STEP_RE.search(text):
            raise SystemExit(f"{name} #{i}: step pattern")
        if re.match(r"^\d{3}、", text):
            raise SystemExit(f"{name} #{i}: already numbered?")
        if len(text.strip()) < 12:
            raise SystemExit(f"{name} #{i}: too short")
    dups = [k for k, v in Counter(items).items() if v > 1]
    if dups:
        raise SystemExit(f"{name}: duplicate lines: {dups[:3]}")

    def cjk_prefix(s: str, n: int = 8) -> str:
        chars = re.findall(r"[\u4e00-\u9fff]", s)
        return "".join(chars[:n])

    open_c = Counter(cjk_prefix(t) for t in items if cjk_prefix(t))
    bad = [(k, v) for k, v in open_c.items() if v >= 4]
    if bad:
        raise SystemExit(f"{name}: repeated openings: {bad[:5]}")
    starts = Counter(t[:18] for t in items if len(t) >= 18)
    if starts and starts.most_common(1)[0][1] >= 4:
        raise SystemExit(f"{name}: repeated 18-char starts: {starts.most_common(1)}")
    for label, value in (("title", title), ("author", author)):
        if value and sum(value in t for t in items) >= 2:
            raise SystemExit(f"{name}: repeated {label}")


def atomic_write(path: Path, data: dict) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def write_book(filename: str, highlights: list[str], tags: list[str], summary: str) -> dict:
    path = ROOT / filename
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)
    numbered = [f"{i:03d}、{t}" for i, t in enumerate(highlights, 1)]
    data["chatgptHighlights"] = numbered
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = CAPTURED
    data["updatedAt"] = UPDATED
    data["tags"] = tags
    data["summary"] = summary
    atomic_write(path, data)
    with path.open("r", encoding="utf-8-sig") as f:
        check = json.load(f)
    ok = (
        len(check["chatgptHighlights"]) == 150
        and check["chatgptStatus"] == "complete"
        and check["highlightsSource"] == "grok"
        and check["updatedAt"] == UPDATED
        and check["chatgptHighlights"][0].startswith("001、")
        and check["chatgptHighlights"][-1].startswith("150、")
    )
    return {"file": filename, "count": len(check["chatgptHighlights"]), "ok": ok, "title": check.get("title")}


def main() -> None:
    if not BOOKS:
        raise SystemExit("BOOKS not populated")
    results = []
    for name, items, tags, summary in BOOKS:
        path = ROOT / name
        with path.open("r", encoding="utf-8-sig") as f:
            meta = json.load(f)
        validate(name, items, meta.get("title", ""), meta.get("author", ""))
        results.append(write_book(name, items, tags, summary))
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
