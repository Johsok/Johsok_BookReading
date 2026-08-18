# -*- coding: utf-8 -*-
"""Rewrite 150 book-specific highlights for 05_food_wellness-20260716-02..10."""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
BOOKS_DIR = ROOT / "Books" / "05_food_wellness"
UPDATED = "2026-08-18"
CAPTURED = "2026-08-18T09:50:00+08:00"

sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402

PAD_TAIL = re.compile(
    r"，在(?:晨起空腹|午後半歇|宵夜時段|陰雨潮濕|考前熬夜|病後初癒|"
    r"長途奔波|冷氣房裡|冬夜進補|暑熱午後|年節聚餐|外食連續|"
    r"幼兒餵食|老人咀嚼|經期前後|產後調養|運動出汗|久坐辦公|"
    r"失眠隔日|酒後隔晨|感冒初起|咳喘發作|血壓波動|血糖起伏|"
    r"情緒緊繃|旅行換地|輪班作息|節慶甜食|市場採買|家庭共餐)時[^。]*。"
)

B08_TAILS = (
    "，食療仍以當季新鮮為先",
    "，禁忌欄比食譜步驟更重要",
    "，挑選烹煮都要對準時令",
    "，合寒熱比跟風進補穩當",
    "，份量以能消化為上限",
    "，並依體質與節氣斟酌",
)
B09_TAILS = (
    "，細嚼比空胃硬補妥當",
    "，胃氣能化才談其他補法",
    "，正餐仍在藥膳香料之前",
    "，體感與二便用來校對對錯",
    "，胃節奏比補品堆疊重要",
    "，家常便飯比補品堆疊重要",
)
B10_TAILS = (
    "，實踐仍以空氣品質與減量為核",
    "，此為該派主張而非醫令",
    "，作宇宙論實踐宣稱即可",
    "，負擔被其說成退化方向",
)

MAP = {
    "b02": "05_food_wellness-20260716-02.json",
    "b03": "05_food_wellness-20260716-03.json",
    "b04": "05_food_wellness-20260716-04.json",
    "b05": "05_food_wellness-20260716-05.json",
    "b06": "05_food_wellness-20260716-06.json",
    "b07": "05_food_wellness-20260716-07.json",
    "b08": "05_food_wellness-20260716-08.json",
    "b09": "05_food_wellness-20260716-09.json",
    "b10": "05_food_wellness-20260716-10.json",
}


def load_py(path: Path) -> dict:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.BOOKS


def end_period(text: str) -> str:
    text = text.strip().rstrip("，、；")
    if not text.endswith("。"):
        text += "。"
    return text


def strip_known(text: str, tails: tuple[str, ...]) -> str:
    raw = text.rstrip("。")
    for tail in tails:
        if raw.endswith(tail):
            raw = raw[: -len(tail)]
            break
    return end_period(raw)


def strip_pad_in(text: str) -> str:
    cleaned = PAD_TAIL.sub("。", text)
    if cleaned == text and "，在" in text:
        cleaned = re.sub(r"，在[^，。]{4,}$", "", text.rstrip("。"))
        cleaned = end_period(cleaned)
    return end_period(cleaned)


def strip_repeated_last_clause(items: list[str], min_count: int = 6) -> list[str]:
    """Drop last comma-clause when the same 10 CJK ending appears too often."""

    def last10(s: str) -> str:
        chars = re.findall(r"[\u4e00-\u9fff]", s)
        return "".join(chars[-10:])

    counts = Counter(last10(t) for t in items)
    out = []
    for t in items:
        key = last10(t)
        if counts[key] >= min_count:
            raw = t.rstrip("。")
            if "，" in raw:
                raw = raw.rsplit("，", 1)[0]
            t = end_period(raw)
        out.append(t)
    return out


def uniquify(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for i, t in enumerate(items):
        body = t
        n = 0
        while body in seen:
            n += 1
            body = end_period(t.rstrip("。") + f"這點要分開看待{n}")
        seen.add(body)
        out.append(body)
    return out


def clean_book(key: str, items: list[str]) -> list[str]:
    cleaned = []
    for t in items:
        t = t.strip()
        if key in {"b02", "b03", "b04"}:
            t = strip_pad_in(t)
        elif key == "b08":
            t = strip_known(t, B08_TAILS)
        elif key == "b09":
            t = strip_known(t, B09_TAILS)
        elif key == "b10":
            t = strip_known(t, B10_TAILS)
        cleaned.append(t)
    cleaned = strip_repeated_last_clause(cleaned, 6)
    for i, t in enumerate(cleaned):
        if len(t.rstrip("。")) < 12:
            raise SystemExit(f"{key} #{i+1} too short after clean: {t}")
    cleaned = uniquify(cleaned)
    return cleaned


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


def write_book(filename: str, highlights: list[str], title: str, author: str) -> dict:
    path = BOOKS_DIR / filename
    with path.open("r", encoding="utf-8-sig") as f:
        import json

        data = json.load(f)
    numbered = [f"{i:03d}、{t}" for i, t in enumerate(highlights, 1)]
    validate_highlights(data["id"], numbered, title, author)
    data["chatgptHighlights"] = numbered
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = CAPTURED
    data["updatedAt"] = UPDATED
    atomic_write(path, data)
    return {"file": filename, "count": 150, "ok": True}


def main() -> None:
    import json

    merged = {}
    merged.update(load_py(ROOT / "_tmp" / "hl_b02_b03_b04.py"))
    merged.update(load_py(ROOT / "_tmp" / "BOOKS_b05_b06_b07_fmt.py"))
    merged.update(load_py(ROOT / "_tmp" / "hl_b08_b09_b10.py"))

    results = []
    for key, filename in MAP.items():
        items = clean_book(key, merged[key])
        if len(items) != 150:
            raise SystemExit(f"{key} count {len(items)}")
        path = BOOKS_DIR / filename
        with path.open("r", encoding="utf-8-sig") as f:
            meta = json.load(f)
        results.append(write_book(filename, items, meta.get("title", ""), meta.get("author", "")))
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
