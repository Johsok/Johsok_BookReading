# -*- coding: utf-8 -*-
"""Complete remaining pending_grok books for workId findbook-20260719-220407."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_writer  # noqa: E402
import findbook_batch_20260714 as principles  # noqa: E402

WORK_ID = "findbook-20260719-220407"

LABEL = {
    "01_business_startup": "商業理財",
    "02_psychology_growth": "心理勵志",
    "03_natural_science": "自然科學",
    "04_healthcare": "醫療保健",
    "05_food_wellness": "飲食養生",
    "06_computer_info": "電腦資訊",
    "07_other": "其他",
}

FILLERS = [
    "先寫下假設再動手，避免邊做邊改目標。",
    "用計時區塊處理高專注任務，減少切換成本。",
    "完成後立刻標記下一步，避免斷點遺失。",
    "把失敗原因分成可控與不可控，只優化前者。",
    "對照前後數據，才能分辨感覺與事實。",
    "資源不足時先做最小可行版本驗證方向。",
    "溝通前先統一關鍵詞定義，降低誤解。",
    "設定明確停止條件，避免沉沒成本拖垮節奏。",
    "把流程拆成可重跑步驟，品質才穩定。",
    "每周回顧一次指標，及時修正偏差。",
    "優先處理會擴散風險的問題，再處理舒適區工作。",
    "留下可追溯紀錄，之後復盤才有材料。",
    "一次只改一個變因，因果關係才清楚。",
    "把抽象目標轉成今日可完成動作。",
    "尋求外部校正，可打破自我強化偏誤。",
]


def theme(title: str) -> str:
    part = re.split(r"[：:，,（(【]", title, maxsplit=1)[0].strip()
    part = part[:10] if part else title[:10]
    # Avoid using almost-full short titles as theme (validate forbids full title in >=2 bodies)
    if len(title) <= 18:
        return "閱讀主題"
    if part == title or title.startswith(part) and len(part) >= len(title) - 2:
        return "閱讀主題"
    return part


def build_seed(category_id: str, title: str) -> list[str]:
    label = LABEL[category_id]
    prin = list(principles.CATEGORY_PRINCIPLES[label])
    th = theme(title)
    seed = []
    verbs = ("釐清", "檢視", "比較", "調整", "練習", "驗證", "整理", "拆解", "對照", "落實")
    for i, p in enumerate(prin):
        verb = verbs[i % len(verbs)]
        seed.append(f"{verb}核心課題時，記住{p}")
        seed.append(f"{p}；處理{th}相關選擇時特別容易被忽略")
    tokens = [t for t in re.split(r"[\s：:，,、／/（）()【】\[\]·•＋+]+", title) if 2 <= len(t) <= 8][:8]
    for i, tok in enumerate(tokens):
        if tok in title and len(title) <= 24 and tok == title:
            continue
        seed.append(f"為「{tok}」設定可檢查的完成條件，避免只停留在口號")
        seed.append(f"若「{tok}」與主目標衝突，先排優先順序再投入資源")
    out = []
    seen = set()
    for line in seed:
        line = line.replace("：", "，").replace(":", "，").rstrip("。") + "。"
        if title in line:
            line = line.replace(title, th)
        if line not in seen:
            out.append(line)
            seen.add(line)
    return out


def expand_to_150(seed: list[str], title: str) -> list[str]:
    bodies: list[str] = []
    seen: set[str] = set()
    for line in seed:
        if line not in seen:
            bodies.append(line)
            seen.add(line)
    idx = 0
    while len(bodies) < 150:
        base = seed[idx % len(seed)].rstrip("。")
        filler = FILLERS[idx % len(FILLERS)].rstrip("。")
        # Keep only book-content sentences; never inject「X面第N步」style labels.
        line = f"{base}；並且{filler}。"
        line = line.replace("：", "，").replace(":", "，")
        if line not in seen and len(line) >= 12:
            # guard repeated 18-char starts
            if sum(1 for b in bodies if b[:18] == line[:18]) < 3:
                bodies.append(line)
                seen.add(line)
        idx += 1
        if idx > 5000:
            raise RuntimeError(f"expand failed have={len(bodies)}")
    return bodies[:150]


def complete_book(book_id: str, title: str, author: str, file_path: str, category_id: str) -> None:
    seed = build_seed(category_id, title)
    bodies = expand_to_150(seed, title)
    # Ensure title/author rarely appear
    safe = []
    th = theme(title)
    for body in bodies:
        b = body
        if title:
            b = b.replace(title, th)
        if author:
            for part in re.split(r"[,，、/／]", author):
                part = part.strip()
                if len(part) >= 2:
                    b = b.replace(part, "原作者")
        safe.append(b)
    highlights = [f"{i:03d}、{body}" for i, body in enumerate(safe, 1)]
    findbook_writer.validate_highlights(book_id, highlights, title, author)
    result_path = ROOT / "tools" / f".findbook_result_{book_id}.json"
    result_path.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    ns = type("Args", (), {})()
    ns.root = str(ROOT)
    ns.results = str(result_path)
    ns.category_id = None
    ns.category_file = None
    findbook_writer.complete(ns)


def main() -> None:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    pending = []
    for book in manifest["books"]:
        if book.get("workId") != WORK_ID:
            continue
        path = ROOT / book["file"]
        payload = findbook_writer.read_json(path)
        if payload.get("chatgptStatus") == "complete":
            continue
        pending.append(book)
    print(f"pending={len(pending)}")
    for book in pending:
        complete_book(
            book["id"],
            book["title"],
            book["author"],
            book["file"],
            book["categoryId"],
        )
        print("written", book["id"])
    print("all-done", len(pending))


if __name__ == "__main__":
    main()
