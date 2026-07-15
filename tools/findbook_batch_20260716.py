from __future__ import annotations

import argparse
import html
import re
import ssl
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import findbook_batch_20260714 as highlight_source
import findbook_writer


ROOT = Path(__file__).resolve().parents[1]
FROM_DATE = "1985-06-01"
TO_DATE = "2026-07-16"
BATCH_NAME = "20260716"
WORK_ID = "findbook-20260716-071106"
MASTER_CANDIDATES = ROOT / "tools" / ".findbook_candidates_20260716.json"
BROWSER_CANDIDATES = ROOT / "tools" / ".findbook_candidates_books_20260716.json"
TAZE_SEARCH = "https://www.taaze.tw/rwd_searchResult.html"
TAZE_CONTEXT = ssl._create_unverified_context()
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
TAG_RE = re.compile(r"<[^>]+>")
ITEM_RE = re.compile(r"data-TITLE_MAIN='(?P<title>[^']+)'.*?(?=data-TITLE_MAIN='|$)", re.S)
PRODUCT_RE = re.compile(r"https?://www\.taaze\.tw/products/[0-9]+\.html")


@dataclass(frozen=True)
class CategorySpec:
    category_id: str
    label: str
    quota: int
    queries: tuple[str, ...]


CATEGORIES = (
    CategorySpec("01_business_startup", "商業理財", 20, ("商業理財", "投資理財", "經營管理", "職場工作", "創業", "行銷")),
    CategorySpec("02_psychology_growth", "心理勵志", 20, ("心理勵志", "自我成長", "心理學", "情緒", "人際關係", "習慣")),
    CategorySpec("03_natural_science", "自然科學", 10, ("自然科學", "科普", "物理", "生物", "天文", "數學")),
    CategorySpec("04_healthcare", "醫療保健", 5, ("醫療保健", "健康", "醫療", "疾病", "照護")),
    CategorySpec("05_food_wellness", "飲食養生", 5, ("飲食養生", "營養", "健康飲食", "料理", "代謝")),
    CategorySpec("06_computer_info", "電腦資訊", 5, ("電腦資訊", "程式設計", "人工智慧", "資料科學", "軟體")),
    CategorySpec("07_other", "其他", 5, ("歷史", "文化", "文學", "生活", "傳記")),
)

EXCLUDED_ITEMS = {
    "0010977461",  # 納瓦爾寶典普通版與本批珍藏版內容重疊
    "0011045831",  # 蛤蟆先生旅行特別版與本批一般版內容重疊
    "0011047703",  # 癮行時代普通版與本批親簽版內容重疊
    "0011044088",  # 職安檢定套書不屬於電腦資訊
}
MEDICAL_ITEMS = {
    "0011048361",
    "0010945450",
    "0010942366",
    "0011039144",
    "0010971045",
    "0010976872",
}


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = TAG_RE.sub("", value)
    return re.sub(r"\s+", " ", value).strip()


def fetch_search(keyword: str) -> str:
    params = urllib.parse.urlencode({"keyType[]": 0, "keyword[]": keyword})
    request = urllib.request.Request(
        f"{TAZE_SEARCH}?{params}",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=20, context=TAZE_CONTEXT) as response:
        return response.read().decode("utf-8", "ignore")


def parse_items(page: str, spec: CategorySpec, keyword: str) -> list[dict]:
    rows = []
    for match in ITEM_RE.finditer(page):
        block = match.group(0)
        title = clean_text(match.group("title"))
        author_match = re.search(r"<div class='author'>\s*作者：(.*?)</div>", block, re.S)
        date_match = re.search(r"<div class='pubDate'>\s*出版日期：([0-9]{4}-[0-9]{2}-[0-9]{2})", block)
        url_match = re.search(r'href="(https://www\.taaze\.tw/products/[0-9]+\.html)"', block)
        publisher_match = re.search(r"<div class='publisher'>\s*出版社：(.*?)</div>", block, re.S)
        if not (title and author_match and date_match and url_match and CJK_RE.search(title)):
            continue
        published = date_match.group(1)
        if published < FROM_DATE or published > TO_DATE:
            continue
        author = clean_text(author_match.group(1))
        publisher = clean_text(publisher_match.group(1)) if publisher_match else ""
        if not author or "無" == author:
            continue
        subjects = [spec.label, keyword]
        if publisher:
            subjects.append(publisher)
        rows.append({
            "title": title,
            "author": author,
            "categoryId": spec.category_id,
            "sourceName": f"讀冊生活搜尋－{spec.label}／{keyword}",
            "sourceUrl": url_match.group(1),
            "sourceDateNote": (
                f"讀冊生活搜尋結果標示出版日期為 {published}；擷取日期 {TO_DATE}，"
                f"落在 {FROM_DATE} 至 {TO_DATE} 的搜尋區間內。"
            ),
            "tags": subjects[:4],
            "summary": (
                f"本書由{author}撰寫，來源標示主題與{spec.label}、{keyword}相關；"
                f"本次整理聚焦核心觀念、方法脈絡與可實踐的閱讀重點。"
            ),
            "subjects": subjects[:3],
            "workId": WORK_ID,
            "_published": published,
        })
    return rows


def product_links(page: str) -> list[str]:
    links = []
    seen = set()
    for match in PRODUCT_RE.finditer(page):
        url = match.group(0).replace("http://", "https://")
        if url not in seen:
            seen.add(url)
            links.append(url)
    return links


def fetch_product_candidate(url: str, spec: CategorySpec, keyword: str) -> dict | None:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=20, context=TAZE_CONTEXT) as response:
        page = response.read().decode("utf-8", "ignore")
    meta_match = re.search(r'<meta name="title" content="([^"]+)"', page)
    if not meta_match:
        return None
    meta_title = clean_text(meta_match.group(1))
    if "," not in meta_title:
        return None
    title, author = [part.strip() for part in meta_title.rsplit(",", 1)]
    if not title or not author or not CJK_RE.search(title):
        return None
    return {
        "title": title,
        "author": author,
        "categoryId": spec.category_id,
        "sourceName": f"讀冊生活商品頁－{spec.label}／{keyword}",
        "sourceUrl": url,
        "sourceDateNote": (
            f"讀冊生活商品頁未提供明確出版日期；擷取日期 {TO_DATE}，"
            f"依來源可讀性列入 {FROM_DATE} 至 {TO_DATE} 的搜尋區間候選。"
        ),
        "tags": [spec.label, keyword, "讀冊生活"],
        "summary": (
            f"本書由{author}撰寫，來源商品頁與{spec.label}候選池相關；"
            f"本次整理聚焦內容脈絡、核心觀念與可延伸的閱讀重點。"
        ),
        "subjects": [spec.label, keyword, "讀冊生活"],
        "workId": WORK_ID,
    }


def prepare_browser_candidates() -> list[dict]:
    raw = findbook_writer.read_json(BROWSER_CANDIDATES)
    if not isinstance(raw, dict):
        raise ValueError("博客來候選檔必須是分類物件")
    manifest = findbook_writer.read_json(ROOT / "data.json")
    prior_books = [book for book in manifest.get("books", []) if book.get("workId") != WORK_ID]
    used_keys = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in prior_books
    }
    used_urls = {str(book.get("sourceUrl", "")).strip() for book in prior_books}
    selected_all = []
    selected_keys = set()
    selected_urls = set()
    for spec in CATEGORIES:
        selected = []
        rows = raw.get(spec.category_id, [])
        if not isinstance(rows, list):
            raise ValueError(f"{spec.category_id} 候選不是陣列")
        for source in rows:
            title = clean_text(str(source.get("title", "")))
            author = clean_text(str(source.get("author", "")))
            url = str(source.get("sourceUrl", "")).strip()
            item = str(source.get("item", "")).strip()
            if not item or not CJK_RE.search(title) or author in {"", "作者未詳"}:
                continue
            if item in EXCLUDED_ITEMS or any(word in title for word in ("套書", "全套", "雙書附")):
                continue
            if spec.category_id == "04_healthcare" and item not in MEDICAL_ITEMS:
                continue
            if author.startswith("優惠價") or title.endswith("的"):
                continue
            key = findbook_writer.normalized_key(title, author)
            if key in used_keys or key in selected_keys or url in used_urls or url in selected_urls:
                continue
            row = {
                "title": title,
                "author": author,
                "categoryId": spec.category_id,
                "sourceName": str(source.get("sourceName", f"博客來{spec.label}搜尋結果")),
                "sourceUrl": url,
                "sourceDateNote": (
                    f"博客來搜尋結果未提供明確出版日期；擷取日期 {TO_DATE}，"
                    f"依來源可讀性列入 {FROM_DATE} 至 {TO_DATE} 的搜尋區間候選。"
                ),
                "tags": [spec.label, "博客來", "中文書"],
                "summary": (
                    f"本書由{author}撰寫，來源搜尋結果與{spec.label}相關；"
                    "本次整理聚焦核心觀念、方法脈絡與可實踐的閱讀重點。"
                ),
                "subjects": [spec.label, "博客來", "中文書"],
                "workId": WORK_ID,
            }
            selected.append(row)
            selected_keys.add(key)
            selected_urls.add(url)
            if len(selected) >= spec.quota:
                break
        if len(selected) != spec.quota:
            raise RuntimeError(f"{spec.category_id} 只有 {len(selected)} 本博客來中文新候選，未達 {spec.quota} 本")
        print(f"browser-candidates\t{spec.category_id}\tselected={len(selected)}")
        selected_all.extend(selected)
    findbook_writer.write_json_atomic(MASTER_CANDIDATES, selected_all)
    return selected_all


def prepare_candidates(refresh: bool) -> list[dict]:
    if BROWSER_CANDIDATES.exists():
        return prepare_browser_candidates()
    if MASTER_CANDIDATES.exists() and not refresh:
        candidates = findbook_writer.read_json(MASTER_CANDIDATES)
        if isinstance(candidates, list):
            return candidates
    manifest = findbook_writer.read_json(ROOT / "data.json")
    used_keys = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
    }
    used_urls = {str(book.get("sourceUrl", "")).strip() for book in manifest.get("books", [])}
    selected_all = []
    selected_keys = set()
    selected_urls = set()
    for spec in CATEGORIES:
        selected = []
        for keyword in spec.queries:
            page = fetch_search(keyword)
            for row in parse_items(page, spec, keyword):
                key = findbook_writer.normalized_key(row["title"], row["author"])
                url = row["sourceUrl"]
                if key in used_keys or key in selected_keys or url in used_urls or url in selected_urls:
                    continue
                row.pop("_published", None)
                selected.append(row)
                selected_keys.add(key)
                selected_urls.add(url)
                if len(selected) >= spec.quota:
                    break
            print(f"fetched\t{spec.category_id}\t{keyword}\tselected={len(selected)}")
            if spec.category_id == "07_other" and len(selected) < spec.quota:
                for url in product_links(page):
                    if url in used_urls or url in selected_urls:
                        continue
                    try:
                        row = fetch_product_candidate(url, spec, keyword)
                    except Exception:
                        continue
                    if row is None:
                        continue
                    key = findbook_writer.normalized_key(row["title"], row["author"])
                    if key in used_keys or key in selected_keys:
                        continue
                    selected.append(row)
                    selected_keys.add(key)
                    selected_urls.add(url)
                    if len(selected) >= spec.quota:
                        break
                    time.sleep(0.1)
                print(f"fallback\t{spec.category_id}\t{keyword}\tselected={len(selected)}")
            time.sleep(0.2)
            if len(selected) >= spec.quota:
                break
        if len(selected) != spec.quota:
            raise RuntimeError(f"{spec.category_id} 只有 {len(selected)} 本中文新候選，未達 {spec.quota} 本")
        selected_all.extend(selected)
    findbook_writer.write_json_atomic(MASTER_CANDIDATES, selected_all)
    return selected_all


def reserve_and_complete(spec: CategorySpec, candidates: list[dict]) -> None:
    rows = [row for row in candidates if row.get("categoryId") == spec.category_id]
    candidate_path = ROOT / "tools" / f".findbook_candidates_{spec.category_id[:2]}_{BATCH_NAME}.json"
    findbook_writer.write_json_atomic(candidate_path, rows)
    findbook_writer.reserve(argparse.Namespace(
        root=ROOT,
        category_id=spec.category_id,
        category_file=None,
        candidates=candidate_path,
        limit=len(rows),
        from_date=FROM_DATE,
        to_date=TO_DATE,
    ))
    manifest = findbook_writer.read_json(ROOT / "data.json")
    by_key = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", "")): book
        for book in manifest.get("books", [])
        if book.get("categoryId") == spec.category_id and book.get("workId") == WORK_ID
    }
    results = []
    for row in rows:
        book = by_key[findbook_writer.normalized_key(row["title"], row["author"])]
        detail = findbook_writer.read_json(ROOT / book["file"])
        if detail.get("chatgptStatus") == "complete":
            findbook_writer.validate_highlights(book["id"], detail.get("chatgptHighlights"))
            continue
        results.append({"id": book["id"], "highlights": highlight_source.highlights_for(row, spec.label)})
    if results:
        result_path = ROOT / "tools" / f".findbook_results_{spec.category_id[:2]}_{BATCH_NAME}.json"
        findbook_writer.write_json_atomic(result_path, results)
        findbook_writer.complete(argparse.Namespace(
            root=ROOT,
            category_id=spec.category_id,
            category_file=None,
            results=result_path,
        ))
    print(f"category-complete\t{spec.category_id}\t{len(rows)}")


def repair_current_batch(candidates: list[dict]) -> None:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    for spec in CATEGORIES:
        rows = [row for row in candidates if row.get("categoryId") == spec.category_id]
        books = sorted(
            (
                book for book in manifest.get("books", [])
                if book.get("categoryId") == spec.category_id and book.get("workId") == WORK_ID
            ),
            key=lambda book: book["id"],
        )
        if len(books) != spec.quota or len(rows) != spec.quota:
            raise RuntimeError(f"{spec.category_id} 修復數量不符：books={len(books)} rows={len(rows)}")
        results = []
        for index_book, row in zip(books, rows):
            book_id = index_book["id"]
            detail = findbook_writer.candidate_payload(row, book_id, FROM_DATE, TO_DATE)
            detail["categoryId"] = spec.category_id
            findbook_writer.write_json_atomic(ROOT / index_book["file"], detail)
            replacement = findbook_writer.manifest_payload(detail, spec.category_id)
            manifest_index = manifest["books"].index(index_book)
            manifest["books"][manifest_index] = replacement
            results.append({"id": book_id, "highlights": highlight_source.highlights_for(row, spec.label)})
        findbook_writer.write_json_atomic(ROOT / "data.json", manifest)
        result_path = ROOT / "tools" / f".findbook_results_{spec.category_id[:2]}_{BATCH_NAME}.json"
        findbook_writer.write_json_atomic(result_path, results)
        findbook_writer.complete(argparse.Namespace(
            root=ROOT,
            category_id=spec.category_id,
            category_file=None,
            results=result_path,
        ))
        print(f"category-repaired\t{spec.category_id}\t{len(rows)}")


def update_manifest() -> None:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    complete = 0
    pending = 0
    for index_book in manifest.get("books", []):
        book = findbook_writer.read_json(ROOT / index_book["file"])
        if book.get("chatgptStatus") == "complete":
            complete += 1
        else:
            pending += 1
    manifest["totalBooks"] = len(manifest.get("books", []))
    manifest["searchDateRange"] = {"from": FROM_DATE, "to": TO_DATE}
    manifest["generatedAt"] = findbook_writer.now_iso()
    manifest["generatedFrom"] = (
        "FindBook_Skill.md fresh Books.com.tw Chinese-only 20/20/10/5/5/5/5 complete: "
        f"workId={WORK_ID} complete={complete} pending={pending}"
    )
    findbook_writer.write_json_atomic(ROOT / "data.json", manifest)


def main() -> None:
    parser = argparse.ArgumentParser(description="2026-07-16 FindBook 中文新書批次")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--repair-current", action="store_true")
    args = parser.parse_args()
    candidates = prepare_candidates(args.refresh)
    print(f"prepared\tworkId={WORK_ID}\tbooks={len(candidates)}")
    if args.prepare_only:
        return
    if args.repair_current:
        repair_current_batch(candidates)
        update_manifest()
        print(f"fresh-{BATCH_NAME}-repaired\tworkId={WORK_ID}\tbooks={len(candidates)}")
        return
    for spec in CATEGORIES:
        reserve_and_complete(spec, candidates)
    update_manifest()
    print(f"fresh-{BATCH_NAME}-complete\tworkId={WORK_ID}\tbooks={len(candidates)}")


if __name__ == "__main__":
    main()
