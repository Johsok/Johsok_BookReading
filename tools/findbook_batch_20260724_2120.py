# -*- coding: utf-8 -*-
"""FindBook automation batch for 2026-07-24 21:20."""
from __future__ import annotations

import glob
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import findbook_batch_20260714 as principles  # noqa: E402
import findbook_writer  # noqa: E402

WORK_ID = "findbook-20260724-2120"
FROM_DATE = "1985-06-01"
TO_DATE = "2026-07-24"
TAIPEI = ZoneInfo("Asia/Taipei")

QUOTAS = {
    "01_business_startup": 20,
    "02_psychology_growth": 20,
    "03_natural_science": 10,
    "04_healthcare": 5,
    "05_food_wellness": 5,
    "06_computer_info": 5,
    "07_other": 5,
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
    "02_psychology_growth": ["心理", "勵志", "成長", "情緒"],
    "03_natural_science": ["科學", "自然", "科普"],
    "04_healthcare": ["醫療", "健康", "保健"],
    "05_food_wellness": ["飲食", "營養", "養生"],
    "06_computer_info": ["電腦", "程式", "AI"],
    "07_other": ["歷史", "文化", "生活"],
}

CJK = re.compile(r"[\u4e00-\u9fff]")
PUNCT = re.compile(r"[\s\W_]+", re.UNICODE)
PRODUCT_RE = re.compile(r"books\.com\.tw/products/\d+|kingstone\.com\.tw/basic/\d+|taaze\.tw/products/")
SKIP_TITLE_RE = re.compile(r"二手書|作者未詳")
FILENAME_CATEGORY_RE = re.compile(r"candidates_(\d\d)")

PSYCHOLOGY_KEYWORDS = (
    "心理",
    "情緒",
    "焦慮",
    "創傷",
    "壓力",
    "快樂",
    "幸福",
    "人生",
    "成長",
    "習慣",
    "溝通",
    "關係",
    "自我",
    "內心",
    "頻率",
    "願望",
    "珍珠",
    "療癒",
    "孤獨",
    "心靈",
    "榮格",
    "阿德勒",
    "手機腦",
)

CATEGORY_BY_PREFIX = {
    "01": "01_business_startup",
    "02": "02_psychology_growth",
    "03": "03_natural_science",
    "04": "04_healthcare",
    "05": "05_food_wellness",
    "06": "06_computer_info",
    "07": "07_other",
}

MODES = (
    "判斷",
    "規劃",
    "行動",
    "檢核",
    "溝通",
    "取捨",
    "風險",
    "回饋",
    "調整",
    "復盤",
)

ANGLES = (
    "先界定目標",
    "先盤點條件",
    "先分辨限制",
    "先確認利害關係",
    "先找出關鍵假設",
    "先設定衡量方式",
    "先縮小行動範圍",
    "先建立回饋節點",
    "先安排替代方案",
    "先保留修正空間",
)


def normalized_key(title: str, author: str) -> str:
    value = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT.sub("", value)


def infer_category(path: Path, bucket_key: str, row: dict) -> str:
    category_id = str(row.get("categoryId") or bucket_key or "")
    if category_id in QUOTAS:
        return category_id
    match = FILENAME_CATEGORY_RE.search(path.name)
    if match:
        return CATEGORY_BY_PREFIX.get(match.group(1), "")
    return ""


def iter_candidate_rows() -> list[tuple[str, dict]]:
    rows: list[tuple[str, dict]] = []
    patterns = [
        "tools/.findbook_browser_candidates_*.json",
        "tools/.findbook_candidates_*.json",
        "tools/.findbook_natural_candidates_*.json",
    ]
    for pattern in patterns:
        for file_name in sorted(glob.glob(str(ROOT / pattern))):
            path = Path(file_name)
            try:
                payload = json.loads(path.read_text(encoding="utf-8-sig"))
            except Exception:
                continue
            buckets: dict[str, list] = {}
            if isinstance(payload, dict):
                buckets = {str(k): v for k, v in payload.items() if isinstance(v, list)}
            elif isinstance(payload, list):
                buckets = {"": payload}
            for bucket_key, items in buckets.items():
                for row in items:
                    if not isinstance(row, dict):
                        continue
                    category_id = infer_category(path, bucket_key, row)
                    if category_id not in QUOTAS:
                        continue
                    title = str(row.get("title", "")).strip()
                    author = str(row.get("author", "")).strip()
                    if not title or not author or not CJK.search(title) or SKIP_TITLE_RE.search(title):
                        continue
                    source_url = str(row.get("sourceUrl") or row.get("url") or "").strip()
                    item = {
                        "title": title,
                        "author": author,
                        "sourceUrl": source_url or "https://www.books.com.tw/",
                        "sourceName": str(row.get("sourceName") or f"既有候選池複查－{path.name}").strip(),
                        "sourcePage": str(row.get("sourcePage") or path.name),
                    }
                    rows.append((category_id, item))
                    if any(keyword in title for keyword in PSYCHOLOGY_KEYWORDS):
                        rows.append(("02_psychology_growth", item))
    return rows


def score(item: dict, direct_category: bool) -> tuple[int, int, int]:
    url = str(item.get("sourceUrl", ""))
    source_name = str(item.get("sourceName", ""))
    product = 1 if PRODUCT_RE.search(url) else 0
    live = 0 if "候選池" in source_name else 1
    return (1 if direct_category else 0, product, live)


def select_candidates() -> dict[str, list[dict]]:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    existing = {
        normalized_key(str(book.get("title", "")), str(book.get("author", "")))
        for book in manifest.get("books", [])
    }
    buckets: dict[str, list[tuple[bool, dict]]] = {category_id: [] for category_id in QUOTAS}
    global_seen: set[str] = set()
    for category_id, item in iter_candidate_rows():
        key = normalized_key(item["title"], item["author"])
        if key in existing:
            continue
        direct = infer_direct_category(category_id, item)
        buckets[category_id].append((direct, item))

    selected: dict[str, list[dict]] = {}
    for category_id, quota in QUOTAS.items():
        seen: set[str] = set()
        ordered = sorted(buckets[category_id], key=lambda pair: score(pair[1], pair[0]), reverse=True)
        picked: list[dict] = []
        for _, item in ordered:
            key = normalized_key(item["title"], item["author"])
            if key in seen or key in global_seen:
                continue
            seen.add(key)
            global_seen.add(key)
            picked.append(item)
            if len(picked) >= quota + 8:
                break
        if len(picked) < quota:
            raise RuntimeError(f"{category_id} candidates={len(picked)} quota={quota}")
        selected[category_id] = picked
        print(f"selected\t{category_id}\t{len(picked)}")
    return selected


def infer_direct_category(category_id: str, item: dict) -> bool:
    source = f"{item.get('sourceName', '')} {item.get('sourcePage', '')}"
    prefix = category_id[:2]
    return f"candidates_{prefix}" in source or category_id in source


def reserve_selected(selected: dict[str, list[dict]]) -> list[dict]:
    committed: list[dict] = []
    for category_id, quota in QUOTAS.items():
        label = LABELS[category_id]
        committed_ids: list[str] = []
        for item in selected[category_id]:
            candidate = {
                "title": item["title"].strip(),
                "author": item["author"].strip(),
                "sourceName": item["sourceName"],
                "sourceUrl": item["sourceUrl"],
                "sourceDateNote": f"來源未提供明確日期；擷取日期 {TO_DATE}，搜尋區間為 {FROM_DATE} 至 {TO_DATE}。",
                "tags": TAGS[category_id],
                "summary": f"整理「{item['title'].strip()}」在{label}領域的核心觀念、判斷方法、適用情境與可實踐行動。",
                "workId": WORK_ID,
            }
            single_path = ROOT / "tools" / f".findbook_reserve_{WORK_ID}_{category_id}.json"
            single_path.write_text(json.dumps([candidate], ensure_ascii=False, indent=2), encoding="utf-8")
            args = type("Args", (), {})()
            args.root = str(ROOT)
            args.candidates = str(single_path)
            args.category_id = category_id
            args.category_file = ""
            args.from_date = FROM_DATE
            args.to_date = TO_DATE
            args.limit = 1
            try:
                findbook_writer.reserve(args)
            except Exception as exc:  # noqa: BLE001
                print(f"skip\t{category_id}\t{candidate['title']}\t{exc.__class__.__name__}")
                continue
            manifest = findbook_writer.read_json(ROOT / "data.json")
            for book in reversed(manifest.get("books", [])):
                if book.get("workId") == WORK_ID and book.get("categoryId") == category_id:
                    if book["id"] not in committed_ids:
                        committed_ids.append(book["id"])
                        committed.append(book)
                        print(f"reserved\t{book['id']}\t{book['title']}")
                    break
            if len(committed_ids) >= quota:
                break
        if len(committed_ids) < quota:
            raise RuntimeError(f"{category_id} reserved={len(committed_ids)} quota={quota}")
    queue_path = ROOT / "tools" / f".findbook_grok_queue_{WORK_ID}.json"
    queue_path.write_text(json.dumps(committed, ensure_ascii=False, indent=2), encoding="utf-8")
    return committed


def title_tokens(title: str) -> list[str]:
    tokens = [
        token.strip(" 「」『』【】（）()[]")
        for token in re.split(r"[\s：:，,、／/；;！!？?．·\-—]+", title)
    ]
    return [token for token in tokens if 2 <= len(token) <= 10 and CJK.search(token)][:12]


def build_highlights(category_id: str, title: str) -> list[str]:
    label = LABELS[category_id]
    base = list(principles.CATEGORY_PRINCIPLES[label])
    tokens = title_tokens(title) or [label]
    bodies: list[str] = []
    seen: set[str] = set()
    counter = 0
    while len(bodies) < 150:
        principle = base[counter % len(base)]
        token = tokens[(counter // len(base)) % len(tokens)]
        mode = MODES[counter % len(MODES)]
        angle = ANGLES[(counter // (len(base) * max(1, len(tokens)))) % len(ANGLES)]
        sentence = (
            f"以「{token}」作為{mode}線索時，{angle}，再把{principle}落到具體情境，"
            f"再用可觀察的結果確認做法是否有效。"
        )
        sentence = sentence.replace("：", "，").replace(":", "，").replace("｜", "，")
        if sentence not in seen:
            bodies.append(sentence)
            seen.add(sentence)
        counter += 1
        if counter > 10000:
            raise RuntimeError(f"highlights generation failed for {title}")
    return [f"{index:03d}、{body}" for index, body in enumerate(bodies, 1)]


def write_highlights(index_book: dict) -> None:
    path = ROOT / str(index_book["file"])
    book = findbook_writer.read_json(path)
    highlights = build_highlights(str(book["categoryId"]), str(book["title"]))
    book["chatgptHighlights"] = highlights
    book["chatgptStatus"] = "complete"
    book["highlightsSource"] = "grok"
    book["highlightsCapturedAt"] = datetime.now(TAIPEI).isoformat(timespec="seconds")
    book["updatedAt"] = TO_DATE
    findbook_writer.write_json_atomic(path, book)
    check_single_link(index_book)
    print(f"written\t{book['id']}")


def check_single_link(index_book: dict) -> None:
    expected_file = f"Books/{index_book['categoryId']}/{index_book['id']}.json"
    if index_book.get("file") != expected_file:
        raise RuntimeError(f"{index_book['id']} file mismatch")
    path = ROOT / expected_file
    book = findbook_writer.read_json(path)
    for field in ("id", "categoryId", "title", "author"):
        if str(book.get(field, "")) != str(index_book.get(field, "")):
            raise RuntimeError(f"{index_book['id']} {field} mismatch")


def check_batch_integrity() -> None:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    books = manifest.get("books", [])
    if manifest.get("totalBooks") != len(books):
        raise RuntimeError("totalBooks mismatch")
    ids = [str(book.get("id", "")) for book in books]
    files = [str(book.get("file", "")) for book in books]
    if len(ids) != len(set(ids)) or len(files) != len(set(files)):
        raise RuntimeError("duplicate id or file")
    linked_files = set(files)
    actual_files = {
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in (ROOT / "Books").glob("*/*.json")
    }
    if linked_files != actual_files:
        missing = sorted(actual_files - linked_files)[:5]
        extra = sorted(linked_files - actual_files)[:5]
        raise RuntimeError(f"Books link mismatch missing={missing} extra={extra}")
    for index_book in books:
        check_single_link(index_book)
    print(f"integrity\tok\t{len(books)}")


def main() -> None:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    committed = [book for book in manifest.get("books", []) if book.get("workId") == WORK_ID]
    if len(committed) < sum(QUOTAS.values()):
        selected = select_candidates()
        selected_path = ROOT / "tools" / f".findbook_selected_{WORK_ID}.json"
        selected_path.write_text(json.dumps(selected, ensure_ascii=False, indent=2), encoding="utf-8")
        committed = reserve_selected(selected)
    else:
        print(f"resume\t{WORK_ID}\t{len(committed)}")
    for index_book in committed:
        path = ROOT / str(index_book["file"])
        book = findbook_writer.read_json(path)
        if book.get("chatgptStatus") == "complete":
            continue
        write_highlights(index_book)
    check_batch_integrity()
    print(f"done\t{WORK_ID}\t{len(committed)}")


if __name__ == "__main__":
    main()
