# -*- coding: utf-8 -*-
"""Mine unused candidates from prior batch pool files."""
from __future__ import annotations

import glob
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUNCT = re.compile(r"[\s\W_]+", re.UNICODE)
CJK = re.compile(r"[\u4e00-\u9fff]")


def normalized_key(title: str, author: str) -> str:
    value = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT.sub("", value)


def main() -> None:
    manifest = json.loads((ROOT / "data.json").read_text(encoding="utf-8-sig"))
    existing = {
        normalized_key(str(book.get("title", "")), str(book.get("author", "")))
        for book in manifest.get("books", [])
    }
    current = json.loads((ROOT / "tools" / ".findbook_scrape_20260719.json").read_text(encoding="utf-8"))

    mined: dict[str, list[dict]] = {k: [] for k in current}
    patterns = [
        "tools/.findbook_browser_candidates_*.json",
        "tools/.findbook_candidates_*.json",
        "tools/.findbook_natural_candidates_*.json",
    ]
    for pattern in patterns:
        for path in sorted(glob.glob(str(ROOT / pattern)), reverse=True)[:40]:
            try:
                payload = json.loads(Path(path).read_text(encoding="utf-8-sig"))
            except Exception:
                continue
            # list or dict-of-lists
            buckets = {}
            if isinstance(payload, dict):
                for key, value in payload.items():
                    if isinstance(value, list):
                        buckets[key] = value
            elif isinstance(payload, list):
                buckets["unknown"] = payload

            for category_id, rows in buckets.items():
                if category_id not in mined and not category_id.startswith(("01_", "02_", "03_", "04_", "05_", "06_", "07_")):
                    continue
                target = category_id if category_id in mined else None
                for row in rows:
                    title = author = url = ""
                    if isinstance(row, dict):
                        title = str(row.get("title", ""))
                        author = str(row.get("author", ""))
                        url = str(row.get("sourceUrl") or row.get("url") or "")
                        if not target:
                            target = str(row.get("categoryId", ""))
                    elif isinstance(row, (list, tuple)) and len(row) >= 2:
                        title, author = str(row[0]), str(row[1])
                        url = str(row[3]) if len(row) >= 4 else ""
                    if not target or target not in mined:
                        continue
                    if not title or not author or not CJK.search(title):
                        continue
                    key = normalized_key(title, author)
                    if key in existing:
                        continue
                    mined[target].append(
                        {
                            "title": title,
                            "author": author,
                            "sourceUrl": url or "https://www.books.com.tw/",
                            "sourceName": f"既有候選池複查－{Path(path).name}",
                            "sourcePage": path,
                        }
                    )

    # dedupe mined + merge into current if needed
    for category_id, rows in mined.items():
        seen = {normalized_key(item["title"], item["author"]) for item in current.get(category_id, [])}
        added = 0
        for item in rows:
            key = normalized_key(item["title"], item["author"])
            if key in seen or key in existing:
                continue
            seen.add(key)
            current.setdefault(category_id, []).append(item)
            added += 1
        print(f"mined\t{category_id}\tpool_unused={len(rows)}\tadded={added}\ttotal={len(current.get(category_id, []))}")

    out = ROOT / "tools" / ".findbook_scrape_20260719.json"
    out.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")
    print("saved")


if __name__ == "__main__":
    main()
