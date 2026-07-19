# -*- coding: utf-8 -*-
"""Select 38 new books and reserve via findbook_writer."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_writer  # noqa: E402

WORK_ID = "findbook-20260719-220407"
FROM_DATE = "2000-06-19"
TO_DATE = "2026-07-19"

QUOTAS = {
    "01_business_startup": 10,
    "02_psychology_growth": 10,
    "03_natural_science": 10,
    "04_healthcare": 3,
    "05_food_wellness": 2,
    "06_computer_info": 1,
    "07_other": 2,
}

LABELS = {
    "01_business_startup": "商業理財",
    "02_psychology_growth": "心理勵志",
    "03_natural_science": "自然科學",
    "04_healthcare": "醫療保健",
    "05_food_wellness": "飲食養生",
    "06_computer_info": "電腦資訊",
    "07_other": "其他",
}

TAGS = {
    "01_business_startup": ["商業", "投資", "創業", "理財"],
    "02_psychology_growth": ["心理", "勵志", "成長", "習慣"],
    "03_natural_science": ["科學", "自然", "科普"],
    "04_healthcare": ["醫療", "健康", "保健"],
    "05_food_wellness": ["飲食", "營養", "養生"],
    "06_computer_info": ["電腦", "程式", "AI"],
    "07_other": ["歷史", "文化", "生活"],
}

CJK = re.compile(r"[\u4e00-\u9fff]")
PRODUCT_RE = re.compile(r"books\.com\.tw/products/\d+|kingstone\.com\.tw/basic/\d+|taaze\.tw/products/")


def score(item: dict) -> tuple:
    url = str(item.get("sourceUrl", ""))
    name = str(item.get("sourceName", ""))
    # Prefer live scrape over mined pools; prefer concrete product URLs
    live = 0 if "候選池" in name else 1
    product = 1 if PRODUCT_RE.search(url) else 0
    return (live, product, len(str(item.get("title", ""))))


def main() -> None:
    scrape = json.loads((ROOT / "tools" / ".findbook_scrape_20260719.json").read_text(encoding="utf-8"))
    selected: dict[str, list[dict]] = {}
    for category_id, quota in QUOTAS.items():
        rows = [item for item in scrape.get(category_id, []) if CJK.search(item.get("title", "")) and item.get("author")]
        rows = sorted(rows, key=score, reverse=True)
        picked = []
        seen = set()
        for item in rows:
            key = findbook_writer.normalized_key(item["title"], item["author"])
            if key in seen:
                continue
            seen.add(key)
            picked.append(item)
            if len(picked) >= quota + 8:  # buffer for reserve skips
                break
        if len(picked) < quota:
            raise SystemExit(f"{category_id} only has {len(picked)} candidates, need {quota}")
        selected[category_id] = picked
        print(f"pick\t{category_id}\t{len(picked)}")

    # write per-category candidate files and reserve sequentially
    committed_all = []
    manifest0 = findbook_writer.read_json(ROOT / "data.json")
    already = {
        findbook_writer.normalized_key(str(b.get("title", "")), str(b.get("author", ""))): b
        for b in manifest0.get("books", [])
        if b.get("workId") == WORK_ID
    }
    for category_id, quota in QUOTAS.items():
        label = LABELS[category_id]
        # count already reserved for this workId+category
        committed = [
            b["id"]
            for b in manifest0.get("books", [])
            if b.get("workId") == WORK_ID and b.get("categoryId") == category_id
        ]
        committed_all.extend(
            b for b in manifest0.get("books", [])
            if b.get("workId") == WORK_ID and b.get("categoryId") == category_id
        )
        if len(committed) >= quota:
            print(f"category-done\t{category_id}\t{len(committed)}\talready")
            continue

        candidates = []
        for item in selected[category_id]:
            key = findbook_writer.normalized_key(item["title"], item["author"])
            if key in already:
                continue
            url = str(item.get("sourceUrl") or "").strip() or "https://www.books.com.tw/"
            source_name = str(item.get("sourceName") or f"博客來中文書－{label}分類頁")
            candidates.append(
                {
                    "title": item["title"].strip(),
                    "author": item["author"].strip(),
                    "sourceName": source_name,
                    "sourceUrl": url,
                    "sourceDateNote": f"來源未提供明確日期；擷取日期 {TO_DATE}，搜尋區間為 {FROM_DATE} 至 {TO_DATE}。",
                    "tags": TAGS[category_id],
                    "summary": f"整理「{item['title'].strip()}」在{label}領域的核心觀念、判斷方法、適用情境與可實踐行動。",
                    "workId": WORK_ID,
                }
            )
        cand_path = ROOT / "tools" / f".findbook_candidates_{category_id}_20260719.json"
        cand_path.write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")

        # reserve one-by-one until quota
        for candidate in candidates:
            if len(committed) >= quota:
                break
            single = ROOT / "tools" / f".findbook_reserve_one_{category_id}.json"
            single.write_text(json.dumps([candidate], ensure_ascii=False, indent=2), encoding="utf-8")
            ns = type("Args", (), {})()
            ns.root = str(ROOT)
            ns.candidates = str(single)
            ns.category_id = category_id
            ns.category_file = ""
            ns.from_date = FROM_DATE
            ns.to_date = TO_DATE
            ns.limit = 1
            try:
                findbook_writer.reserve(ns)
                # read last committed id from book dir / manifest
                manifest = findbook_writer.read_json(ROOT / "data.json")
                for book in reversed(manifest["books"]):
                    if book.get("workId") == WORK_ID and book.get("categoryId") == category_id:
                        if book["id"] not in committed:
                            committed.append(book["id"])
                            committed_all.append(book)
                            print(f"ok\t{book['id']}")
                        break
            except Exception as exc:  # noqa: BLE001
                print(f"skip\t{exc.__class__.__name__}")
                continue
        if len(committed) < quota:
            raise SystemExit(f"{category_id} reserved {len(committed)} < {quota}")
        print(f"category-done\t{category_id}\t{len(committed)}")

    # rebuild full queue from manifest for this workId
    manifest = findbook_writer.read_json(ROOT / "data.json")
    queue = [book for book in manifest.get("books", []) if book.get("workId") == WORK_ID]
    queue_path = ROOT / "tools" / f".findbook_grok_queue_{WORK_ID}.json"
    queue_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"queue\t{len(queue)}")
    print(f"WORK_ID={WORK_ID}")


if __name__ == "__main__":
    main()
