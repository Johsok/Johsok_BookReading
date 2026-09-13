# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_scraper as s  # noqa: E402
import findbook_writer as w  # noqa: E402

WORK_ID = "findbook-20260913-1938"
FROM_DATE = "1986-09-13"
TO_DATE = "2021-09-13"


def related_from_books_detail(html: str) -> list[dict]:
    items = s.parse_books_list(html)
    # 博客來詳情頁也會有「看過這本書的人」連結。
    extra = []
    seen = {item["sourceUrl"] for item in items}
    for match in re.finditer(r"https://www\.books\.com\.tw/products/(001\d{7})", html):
        url = f"https://www.books.com.tw/products/{match.group(1)}"
        if url in seen:
            continue
        seen.add(url)
        extra.append(
            {
                "title": "",
                "author": "",
                "sourceUrl": url,
                "published": "",
                "sourceSite": "博客來",
            }
        )
    return items + extra


def main() -> None:
    existing_keys = s.load_existing_keys(ROOT)
    seen: set[str] = set()
    found: list[dict] = []

    def take(item: dict, source_name: str) -> None:
        if len(found) >= 6:
            return
        title = str(item.get("title") or "")
        if re.search(r"简体|簡體|漫畫|Minecraft", title):
            return
        pid = s.BOOKS_PID_RE.search(item.get("sourceUrl") or "")
        if pid and pid.group(1) >= "0010930000":
            return
        item = dict(item)
        item["sourceName"] = source_name
        key = s._accept_item(item, existing_keys, seen, FROM_DATE, TO_DATE, "06_computer_info")
        if not key:
            return
        seen.add(key)
        cand = s.to_candidate(item, "06_computer_info", FROM_DATE, TO_DATE)
        cand["workId"] = WORK_ID
        found.append(cand)
        print("ACCEPT", cand.get("published"), cand["title"], cand["author"], cand["sourceUrl"])

    print("retry TAAZE")
    for list_id, name in s.TAAZE_CLASSIC_LISTS["06_computer_info"]:
        if len(found) >= 6:
            break
        try:
            rows = s.fetch_taaze_tag_items(list_id)
            print(name, len(rows))
        except Exception as exc:  # noqa: BLE001
            print(name, "FAIL", exc)
            continue
        for item in rows:
            take(item, name)

    if len(found) < 6:
        print("博客來 C語言詳情與相關書")
        html = s.fetch_html(
            "https://www.books.com.tw/products/0010360466",
            referer="https://www.books.com.tw/",
        )
        title, author, published = s.parse_books_detail(html)
        print("detail", title, author, published)
        take(
            {
                "title": title or "C語言教學手冊（四版）",
                "author": author or "洪維恩",
                "sourceUrl": "https://www.books.com.tw/products/0010360466",
                "published": published,
                "sourceSite": "博客來",
            },
            "博客來中文書－電腦資訊經典暢銷榜",
        )
        related = related_from_books_detail(html)
        missing = [item for item in related if not item.get("author") or not item.get("title")]
        ready = [item for item in related if item.get("author") and item.get("title")]
        for item in ready:
            take(item, "博客來中文書－電腦資訊經典暢銷榜")
        extra = s._enrich_parallel(
            missing[:16],
            s.parse_books_detail,
            "https://www.books.com.tw/",
            8,
            None,
            print,
            "博客來",
        )
        for item in extra:
            take(item, "博客來中文書－電腦資訊經典暢銷榜")

    print("TOTAL", len(found))
    (ROOT / "tools" / ".findbook_candidates_findbook-20260913-1938.json").write_text(
        json.dumps({"06_computer_info": found}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if len(found) < 5:
        raise SystemExit("computer quota unmet")
    committed = []
    for candidate in found:
        if len(committed) >= 5:
            break
        result = w.reserve_one(ROOT, "06_computer_info", candidate, FROM_DATE, TO_DATE)
        print(result)
        if result.get("status") == "committed":
            committed.append(result["id"])
    if len(committed) != 5:
        raise SystemExit(f"committed {len(committed)}")
    print("IDS", ",".join(committed))


if __name__ == "__main__":
    main()
