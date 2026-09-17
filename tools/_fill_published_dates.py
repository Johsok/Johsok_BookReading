# -*- coding: utf-8 -*-
"""Fill missing data.json published dates from 博客來, then momo."""
from __future__ import annotations

import json
import re
import sys
import time
import unicodedata
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import findbook_scraper as scraper  # noqa: E402
from findbook_writer import (  # noqa: E402
    extract_published_from_html,
    now_iso,
    sort_manifest_books,
    write_json_atomic,
)

PUNCT_RE = re.compile(r"[\s\W_]+", re.UNICODE)
ITEM_RE = re.compile(r"/item/([A-Z0-9]{8,})/", re.I)
MOMO_CODE_RE = re.compile(r"i_code=(\d+)", re.I)
MOMO_DATE_RE = re.compile(
    r"出版日[期]?[：:\s]*((?:19|20)\d{2})[./年\-](\d{1,2})[./月\-](\d{1,2})"
)
GENERIC_AUTHOR_HINTS = (
    "編輯",
    "研究室",
    "研究團隊",
    "編輯部",
    "編輯室",
    "編輯團隊",
    "團隊",
)


def compact(text: object) -> str:
    value = unicodedata.normalize("NFKC", str(text or "")).casefold()
    return PUNCT_RE.sub("", value)


def core_title(text: object) -> str:
    value = unicodedata.normalize("NFKC", str(text or ""))
    value = re.sub(r"[【（\(].*?[】）\)]", "", value)
    value = value.split("：")[0].split(":")[0].split("——")[0].split("—")[0]
    return compact(value)


def titles_match(left: str, right: str) -> bool:
    a = compact(left)
    b = compact(right)
    if not a or not b:
        return False
    if a == b or a in b or b in a:
        return True
    ca = core_title(left)
    cb = core_title(right)
    if ca and cb and (ca == cb or (len(ca) >= 4 and (ca in cb or cb in ca))):
        return True
    return False


def author_tokens(text: object) -> set[str]:
    value = unicodedata.normalize("NFKC", str(text or ""))
    parts = re.split(r"[,，、/|；;＆&]+", value)
    tokens = set()
    for part in parts:
        token = compact(part)
        if len(token) >= 2:
            tokens.add(token)
    return tokens


def authors_overlap(left: str, right: str) -> bool:
    a = author_tokens(left)
    b = author_tokens(right)
    if not a or not b:
        return False
    for item in a:
        for other in b:
            if item in other or other in item:
                return True
    return False


def is_generic_author(author: str) -> bool:
    return any(hint in str(author or "") for hint in GENERIC_AUTHOR_HINTS)


def parse_books_search(html: str) -> list[dict]:
    items: list[dict] = []
    seen: set[str] = set()
    for match in re.finditer(
        r'id="prod-itemlist-([A-Z0-9]+)"[\s\S]{0,1800}?<h4>[\s\S]{0,400}?title="([^"]+)"',
        html,
        re.I,
    ):
        pid = match.group(1)
        title = scraper.strip_html(match.group(2))
        if pid in seen or not title:
            continue
        seen.add(pid)
        block = html[match.start() : match.start() + 1800]
        author = ""
        author_match = re.search(r"class=\"author\"[\s\S]{0,600}", block)
        if author_match:
            author = scraper.strip_html(author_match.group(0))
            author = re.sub(r"^作者", "", author).strip(" /|,，、")
        items.append(
            {
                "title": title,
                "author": author,
                "pid": pid,
                "sourceUrl": f"https://www.books.com.tw/products/{pid}",
            }
        )
    if items:
        return items
    for match in re.finditer(ITEM_RE, html):
        pid = match.group(1)
        if pid in seen or pid.startswith("E"):
            continue
        seen.add(pid)
        items.append(
            {
                "title": "",
                "author": "",
                "pid": pid,
                "sourceUrl": f"https://www.books.com.tw/products/{pid}",
            }
        )
    return items


def pick_books_match(book: dict, candidates: list[dict]) -> dict | None:
    title = str(book.get("title") or "")
    author = str(book.get("author") or "")
    short = len(core_title(title)) < 4
    for item in candidates:
        if item.get("title") and not titles_match(title, item["title"]):
            continue
        if not item.get("title") and short:
            continue
        if short and not authors_overlap(author, item.get("author") or ""):
            continue
        if (
            not is_generic_author(author)
            and item.get("author")
            and not authors_overlap(author, item["author"])
            and not titles_match(title, item.get("title") or "")
        ):
            continue
        if item.get("title") and titles_match(title, item["title"]):
            if short and not authors_overlap(author, item.get("author") or ""):
                continue
            return item
    return None


def fetch_books_published(url: str) -> tuple[str, str, str]:
    html = scraper.fetch_html(url, referer="https://www.books.com.tw/")
    title, author, published = scraper.parse_books_detail(html)
    if not published:
        published = extract_published_from_html(html)
    return title, author, published


def search_books(query: str) -> list[dict]:
    url = (
        "https://search.books.com.tw/search/query/key/"
        + urllib.parse.quote(query)
        + "/cat/all/sort/1/v/1/page/1"
    )
    html = scraper.fetch_html(url, referer="https://search.books.com.tw/")
    return parse_books_search(html)


def parse_momo_search(html: str) -> list[dict]:
    items: list[dict] = []
    seen: set[str] = set()
    for match in re.finditer(
        r'href="([^"]*GoodsDetail\.jsp\?[^"]*i_code=(\d+)[^"]*)"[^>]*>(.*?)</a>',
        html,
        re.I | re.S,
    ):
        code = match.group(2)
        if code in seen:
            continue
        title = scraper.strip_html(match.group(3))
        if not title or len(title) < 2:
            continue
        seen.add(code)
        items.append(
            {
                "title": title,
                "code": code,
                "sourceUrl": "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code="
                + code,
            }
        )
    if items:
        return items
    for match in re.finditer(MOMO_CODE_RE, html):
        code = match.group(1)
        if code in seen:
            continue
        seen.add(code)
        items.append(
            {
                "title": "",
                "code": code,
                "sourceUrl": "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code="
                + code,
            }
        )
    return items[:20]


def fetch_momo_published(url: str) -> tuple[str, str]:
    html = scraper.fetch_html(url, referer="https://www.momoshop.com.tw/")
    title = ""
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    if title_match:
        title = scraper.strip_html(title_match.group(1))
    if not title:
        og = re.search(r'property="og:title"\s+content="([^"]+)"', html, re.I)
        if og:
            title = scraper.strip_html(og.group(1))
    published = ""
    date_match = MOMO_DATE_RE.search(html)
    if date_match:
        published = (
            f"{date_match.group(1)}-{int(date_match.group(2)):02d}-"
            f"{int(date_match.group(3)):02d}"
        )
    if not published:
        published = extract_published_from_html(html)
    return title, published


def search_momo(query: str) -> list[dict]:
    url = (
        "https://www.momoshop.com.tw/search/searchShop.jsp?keyword="
        + urllib.parse.quote(query)
        + "&searchType=1&cateLevel=0&_isFuzzy=0&ent=k"
    )
    html = scraper.fetch_html(url, referer="https://www.momoshop.com.tw/")
    return parse_momo_search(html)


def lookup_book(book: dict) -> dict:
    title = str(book.get("title") or "")
    author = str(book.get("author") or "")
    source_url = str(book.get("sourceUrl") or "")
    result = {
        "id": book.get("id"),
        "title": title,
        "author": author,
        "published": "",
        "source": "",
        "matchedUrl": "",
        "matchedTitle": "",
        "note": "",
    }
    if "books.com.tw/products/" in source_url:
        try:
            found_title, found_author, published = fetch_books_published(source_url)
            if published:
                result.update(
                    {
                        "published": published,
                        "source": "博客來商品頁",
                        "matchedUrl": source_url.split("?")[0],
                        "matchedTitle": found_title,
                        "note": found_author,
                    }
                )
                return result
            result["note"] = "商品頁無日期"
        except Exception as exc:  # noqa: BLE001
            result["note"] = f"商品頁失敗：{exc}"

    queries = []
    for query in (title, f"{title} {author.split(',')[0].split('、')[0]}"):
        query = re.sub(r"\s+", " ", query).strip()
        if query and query not in queries:
            queries.append(query)

    for query in queries:
        try:
            candidates = search_books(query)
        except Exception as exc:  # noqa: BLE001
            result["note"] = f"博客來搜尋失敗：{exc}"
            continue
        picked = pick_books_match(book, candidates)
        if not picked and candidates and titles_match(title, candidates[0].get("title") or ""):
            picked = candidates[0]
        if not picked:
            continue
        try:
            found_title, found_author, published = fetch_books_published(picked["sourceUrl"])
        except Exception as exc:  # noqa: BLE001
            result["note"] = f"博客來詳情失敗：{exc}"
            continue
        use_title = found_title or picked.get("title") or ""
        if use_title and not titles_match(title, use_title):
            continue
        if published:
            result.update(
                {
                    "published": published,
                    "source": "博客來搜尋",
                    "matchedUrl": picked["sourceUrl"],
                    "matchedTitle": use_title,
                    "note": found_author,
                }
            )
            return result

    for query in queries:
        try:
            candidates = search_momo(query)
        except Exception as exc:  # noqa: BLE001
            result["note"] = f"momo搜尋失敗：{exc}"
            continue
        picked = None
        for item in candidates:
            if item.get("title") and titles_match(title, item["title"]):
                picked = item
                break
        if not picked:
            continue
        try:
            found_title, published = fetch_momo_published(picked["sourceUrl"])
        except Exception as exc:  # noqa: BLE001
            result["note"] = f"momo詳情失敗：{exc}"
            continue
        use_title = found_title or picked.get("title") or ""
        if use_title and not titles_match(title, use_title):
            continue
        if published:
            result.update(
                {
                    "published": published,
                    "source": "momo搜尋",
                    "matchedUrl": picked["sourceUrl"],
                    "matchedTitle": use_title,
                }
            )
            return result

    if not result["note"]:
        result["note"] = "博客來與 momo 皆無對應書目"
    return result


def main() -> None:
    lookup_only = "--lookup-only" in sys.argv
    manifest_path = ROOT / "data.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    missing = [
        book
        for book in manifest.get("books") or []
        if not str(book.get("published") or "").strip()
    ]
    print(f"missing {len(missing)}", flush=True)
    results = []
    for index, book in enumerate(missing, start=1):
        print(f"[{index}/{len(missing)}] {book.get('id')}", flush=True)
        row = lookup_book(book)
        results.append(row)
        print(
            f"  -> {row['published'] or 'NONE'} | {row['source'] or row['note']} | {row['matchedTitle'][:40]}",
            flush=True,
        )
        time.sleep(0.15)
    out_path = ROOT / "tools" / "_published_lookup.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    found = sum(1 for row in results if row.get("published"))
    print(f"lookup done {found}/{len(results)}", flush=True)
    if lookup_only:
        return

    by_id = {row["id"]: row for row in results if row.get("published")}
    updated = 0
    for book in manifest.get("books") or []:
        row = by_id.get(book.get("id"))
        if not row:
            continue
        book["published"] = row["published"]
        updated += 1
        file_path = ROOT / str(book.get("file") or "")
        if file_path.is_file():
            payload = json.loads(file_path.read_text(encoding="utf-8-sig"))
            if not str(payload.get("published") or "").strip():
                payload["published"] = row["published"]
                write_json_atomic(file_path, payload)
    sort_manifest_books(manifest)
    manifest["generatedAt"] = now_iso()
    write_json_atomic(manifest_path, manifest)
    print(f"applied {updated}", flush=True)


if __name__ == "__main__":
    main()
