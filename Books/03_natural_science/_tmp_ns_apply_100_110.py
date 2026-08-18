# -*- coding: utf-8 -*-
"""Overwrite chatgptHighlights for natural-science books 100-110."""
import importlib.util
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")
STAMP = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
STAMP = STAMP[:-2] + ":" + STAMP[-2:] if len(STAMP) >= 5 else STAMP
UPDATED = "2026-08-18"

PAD_SUFFIXES = (
    "，光學條件一變就更明顯。",
    "，老化後這條路徑往往先出問題。",
    "，否則夜間與近距表現會分家。",
    "，這會直接改寫你看見的對比。",
    "，中心窩與周邊必須分開評估。",
    "，色覺通道的疲勞也會參一腳。",
    "，大腦解釋層也會跟著被帶偏。",
    "，動物比較更能凸顯這項取捨。",
    "，相機類比在這裡剛好會失效。",
    "，檢查時要把照明與屈光分開看。",
    "，價值判斷其實早已在此運作。",
    "，文化發明只是把這層寫得更大。",
    "，笛卡兒式身心切開會把順序講反。",
    "，理性計算仍要站在這層地面上。",
    "，沒有體內地圖就談不上真正在乎。",
    "，意義來自生命過程而非純符號。",
    "，發展順序上身體調節來得更早。",
    "，群體制度多半在延伸這套恆定。",
    "，情緒程式與感受讀數必須分開。",
    "，機器模擬語句替代不了這件事。",
    "，流行病學看的是族群而非命運。",
    "，內污染與外照射策略完全不同。",
    "，非游離來源不該混進這張表。",
    "，公眾恐懼常把量級整個弄亂。",
    "，職業限值與公眾限值差一個數量級。",
    "，修復時間會讓同樣戈雷結果不同。",
    "，比較風險時要先對齊單位。",
    "，測得到不等於已經達到致病劑量。",
    "，兒童與胚胎要用更嚴的合理抑低。",
)


def load_books(name):
    path = ROOT / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.BOOKS


def strip_padding(text):
    changed = True
    while changed:
        changed = False
        for suf in PAD_SUFFIXES:
            if text.endswith(suf) and len(text) - len(suf) >= 12:
                core = text[: -len(suf)].rstrip("，,、 ")
                text = core if core.endswith("。") else core + "。"
                changed = True
    return text


def numbered(items):
    cleaned = [strip_padding(t.strip()) for t in items]
    if len(cleaned) != 150:
        raise SystemExit(f"need 150, got {len(cleaned)}")
    if len(set(cleaned)) != 150:
        dups = [t for t in cleaned if cleaned.count(t) > 1]
        raise SystemExit(f"duplicate after strip: {dups[:3]}")
    for t in cleaned:
        if not t or "｜" in t or t.startswith(("本書", "作者指出")):
            raise SystemExit(f"bad item: {t[:40]}")
    return [f"{i:03d}、{t}" for i, t in enumerate(cleaned, 1)]


def patch(filename, rec):
    path = ROOT / filename
    data = json_load(path)
    data["chatgptHighlights"] = numbered(rec["items"])
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = UPDATED
    if rec.get("summary"):
        data["summary"] = rec["summary"]
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json_dump(data), encoding="utf-8")
    tmp.replace(path)
    print(f"OK {filename} n={len(data['chatgptHighlights'])}")


def json_load(path):
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def json_dump(data):
    import json

    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def main():
    merged = {}
    for name in (
        "_tmp_ns_hl_100_102",
        "_tmp_ns_hl_103_105",
        "_tmp_ns_hl_106_108",
        "_tmp_ns_hl_109_110",
    ):
        merged.update(load_books(name))
    expected = [f"03_natural_science-20260716-{n}.json" for n in range(100, 111)]
    missing = [f for f in expected if f not in merged]
    if missing:
        raise SystemExit(f"missing drafts: {missing}")
    for fn in expected:
        patch(fn, merged[fn])


if __name__ == "__main__":
    main()
