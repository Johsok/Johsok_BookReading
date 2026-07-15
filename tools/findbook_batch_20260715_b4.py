from __future__ import annotations

import argparse
import concurrent.futures
import json
import math
import re
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import findbook_batch_20260714 as highlight_source
import findbook_writer


ROOT = Path(__file__).resolve().parents[1]
FROM_DATE = "2000-06-01"
TO_DATE = "2026-07-15"
BATCH_NAME = "b4"
WORK_ID = "findbook-20260715-194023-b4"
OPEN_LIBRARY_SEARCH = "https://openlibrary.org/search.json"
MASTER_CANDIDATES = ROOT / "tools" / ".findbook_candidates_20260715_b4.json"
BAD_TITLE = re.compile(
    r"\b(?:annual report|proceedings|bibliography|catalogue|newsletter|journal|"
    r"workbook for|summary of|study guide|advances in|international review|"
    r"transactions on|a macat analysis)\b",
    re.IGNORECASE,
)
REJECT_TITLES = {
    "control your mind and master your feelings",
    "dream psychology",
    "sustain me",
    "the green witch",
    "the inner life of animals",
    "the diary of a ceo",
    "girlboss",
    "dark psychology",
    "3am questions",
    "great astronomers",
    "the real world",
    "the diary of a young girl- anne frank",
    "forgotten home apothecary",
    "nutrition & you : core concepts for good health",
    "lost book of herbal remedies",
    "the source legacy workbook",
    "the dictionary of body language",
    "strength training anatomy",
    "sales eq",
    "the third door",
    "pathless path",
    "there's treasure inside",
    "a theory of human motivation",
    "you can heal your life",
    "self heal by design",
    "hands-on machine learning with scikit-learn, keras, and tensorflow",
    "no rules rules",
}
FICTION_SUBJECT = re.compile(
    r"(?:fiction|romance|novel|love stories|juvenile|imaginary|thriller|fantasy|detective)",
    re.IGNORECASE,
)
CATEGORY_REJECT_TITLES = {
    "03_natural_science": {"the wisdom of psychopaths"},
    "07_other": {"life's amazing secrets"},
}


@dataclass(frozen=True)
class CategorySpec:
    category_id: str
    label: str
    quota: int
    queries: tuple[tuple[str, str], ...]


CATEGORIES = (
    CategorySpec(
        "01_business_startup",
        "商業理財",
        30,
        (
            ("business", "商業"),
            ("management", "管理"),
            ("leadership", "領導"),
            ("marketing", "行銷"),
            ("entrepreneurship", "創業"),
            ("personal finance", "個人理財"),
            ("investing", "投資"),
        ),
    ),
    CategorySpec(
        "02_psychology_growth",
        "心理勵志",
        30,
        (
            ("psychology", "心理學"),
            ("self-help", "自我成長"),
            ("personal development", "個人成長"),
            ("mindfulness", "正念"),
            ("motivation", "動機"),
            ("emotional intelligence", "情緒智能"),
            ("relationships", "人際關係"),
        ),
    ),
    CategorySpec(
        "03_natural_science",
        "自然科學",
        10,
        (
            ("popular science", "科普"),
            ("physics", "物理"),
            ("biology", "生物"),
            ("astronomy", "天文"),
            ("mathematics", "數學"),
            ("neuroscience", "神經科學"),
        ),
    ),
    CategorySpec(
        "04_healthcare",
        "醫療保健",
        2,
        (("medicine", "醫學"), ("health", "健康"), ("public health", "公共衛生")),
    ),
    CategorySpec(
        "05_food_wellness",
        "飲食養生",
        2,
        (("nutrition", "營養"), ("healthy eating", "健康飲食"), ("cooking", "料理")),
    ),
    CategorySpec(
        "06_computer_info",
        "電腦資訊",
        2,
        (
            ("programming", "程式設計"),
            ("software engineering", "軟體工程"),
            ("artificial intelligence", "人工智慧"),
            ("computer science", "電腦科學"),
        ),
    ),
    CategorySpec(
        "07_other",
        "其他",
        2,
        (("history", "歷史"), ("culture", "文化"), ("biography", "傳記")),
    ),
)


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalized_title(title: str) -> str:
    return re.sub(r"[\s\W_]+", "", title.casefold())


def unique_authors(values: object) -> list[str]:
    authors = []
    seen = set()
    for value in values or []:
        author = clean(value)
        tokens = [token for token in re.findall(r"\w+", author.casefold()) if len(token) > 1]
        key = "".join((tokens[0], tokens[-1])) if tokens else ""
        if author and key and key not in seen:
            seen.add(key)
            authors.append(author)
    return authors


def fetch_query(query: tuple[str, str]) -> tuple[str, str, list[dict]]:
    subject, focus = query
    params = urllib.parse.urlencode({
        "subject": subject,
        "language": "eng",
        "limit": 100,
        "fields": (
            "key,title,author_name,first_publish_year,subject,"
            "edition_count,ratings_count,ratings_average"
        ),
    })
    request = urllib.request.Request(
        f"{OPEN_LIBRARY_SEARCH}?{params}",
        headers={"User-Agent": "Johsok-BookReading/1.0 (FindBook metadata lookup)"},
    )
    last_error = None
    for attempt in range(2):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return subject, focus, payload.get("docs", [])
        except Exception as error:
            last_error = error
            if attempt == 0:
                time.sleep(1)
    raise RuntimeError(f"Open Library 查詢失敗：{subject}: {last_error}")


def candidate_score(doc: dict, rank: int) -> float:
    editions = int(doc.get("edition_count") or 0)
    ratings = int(doc.get("ratings_count") or 0)
    average = float(doc.get("ratings_average") or 0)
    year = int(doc.get("first_publish_year") or 0)
    return (120 - rank) + min(editions, 80) * 2 + math.log1p(ratings) * 18 + average * 4 + (year - 2000) * 0.25


def candidate_from_doc(doc: dict, spec: CategorySpec, focus: str, rank: int) -> dict | None:
    title = clean(doc.get("title"))
    authors = unique_authors(doc.get("author_name", []))
    author = "、".join(authors[:4])
    work_key = clean(doc.get("key"))
    year = doc.get("first_publish_year")
    if not title or not author or not work_key.startswith("/works/"):
        return None
    if "?" in author:
        return None
    if not isinstance(year, int) or not 2001 <= year <= 2026:
        return None
    if (
        len(title) < 4
        or len(title) > 140
        or BAD_TITLE.search(title)
        or title.casefold() in REJECT_TITLES
        or title.casefold() in CATEGORY_REJECT_TITLES.get(spec.category_id, set())
    ):
        return None
    all_subjects = [clean(item) for item in doc.get("subject", []) if clean(item)]
    if any(FICTION_SUBJECT.search(subject) for subject in all_subjects):
        return None
    if spec.category_id == "03_natural_science" and re.match(
        r"^(?:advances in|international review|college )", title, re.IGNORECASE
    ):
        return None
    raw_subjects = [item for item in all_subjects if 2 <= len(item) <= 28]
    subjects = list(dict.fromkeys([focus, *raw_subjects[:2]]))[:3]
    source_url = f"https://openlibrary.org{work_key}"
    return {
        "title": title,
        "author": author,
        "categoryId": spec.category_id,
        "sourceName": f"Open Library {spec.label}主題書目",
        "sourceUrl": source_url,
        "sourceDateNote": (
            f"Open Library 書目標示初版年份為 {year}；擷取日期 {TO_DATE}，"
            f"落在 {FROM_DATE} 至 {TO_DATE} 的搜尋區間內。"
        ),
        "tags": [spec.label, *subjects],
        "summary": (
            f"《{title}》由{author}撰寫，書目主題涵蓋{'、'.join(subjects)}；"
            f"本次依{spec.label}閱讀目的整理核心觀點、證據與可實踐方法。"
        ),
        "subjects": subjects,
        "firstPublishYear": year,
        "workId": WORK_ID,
        "_score": candidate_score(doc, rank),
    }


def prepare_candidates() -> list[dict]:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    used_keys = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
    }
    used_urls = {clean(book.get("sourceUrl")) for book in manifest.get("books", [])}
    used_titles = {normalized_title(clean(book.get("title"))) for book in manifest.get("books", [])}
    selected_all = []
    for spec in CATEGORIES:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            batches = list(executor.map(fetch_query, spec.queries))
        pool = {}
        for _subject, focus, docs in batches:
            for rank, doc in enumerate(docs):
                candidate = candidate_from_doc(doc, spec, focus, rank)
                if candidate is None:
                    continue
                key = findbook_writer.normalized_key(candidate["title"], candidate["author"])
                url = candidate["sourceUrl"]
                title_key = normalized_title(candidate["title"])
                if key in used_keys or url in used_urls or title_key in used_titles:
                    continue
                current = pool.get(title_key)
                if current is None or candidate["_score"] > current["_score"]:
                    pool[title_key] = candidate
        buffer_target = spec.quota + max(2, math.ceil(spec.quota * 0.2))
        ordered = sorted(pool.values(), key=lambda item: (-item["_score"], item["title"].casefold()))
        if len(ordered) < buffer_target:
            raise RuntimeError(
                f"{spec.category_id} 合格候選只有 {len(ordered)} 本，未達緩衝目標 {buffer_target} 本"
            )
        selected = ordered[:spec.quota]
        for candidate in selected:
            candidate.pop("_score", None)
            key = findbook_writer.normalized_key(candidate["title"], candidate["author"])
            used_keys.add(key)
            used_urls.add(candidate["sourceUrl"])
            used_titles.add(normalized_title(candidate["title"]))
        selected_all.extend(selected)
        print(f"candidate-ready\t{spec.category_id}\tselected={len(selected)}\tpool={len(ordered)}")
    findbook_writer.write_json_atomic(MASTER_CANDIDATES, selected_all)
    print(f"prepared\tworkId={WORK_ID}\tbooks={len(selected_all)}")
    return selected_all


def load_and_validate_candidates() -> list[dict]:
    candidates = findbook_writer.read_json(MASTER_CANDIDATES)
    if not isinstance(candidates, list):
        raise ValueError("候選檔必須是 JSON 陣列")
    counts = {spec.category_id: 0 for spec in CATEGORIES}
    work_ids = set()
    keys = set()
    urls = set()
    for candidate in candidates:
        category_id = candidate.get("categoryId")
        if category_id not in counts:
            raise ValueError(f"未知候選分類：{category_id}")
        counts[category_id] += 1
        work_ids.add(candidate.get("workId"))
        key = findbook_writer.normalized_key(candidate.get("title", ""), candidate.get("author", ""))
        if key in keys or candidate.get("sourceUrl") in urls:
            raise ValueError(f"候選檔內重複：{candidate.get('title')}")
        keys.add(key)
        urls.add(candidate.get("sourceUrl"))
    expected = {spec.category_id: spec.quota for spec in CATEGORIES}
    if counts != expected or work_ids != {WORK_ID}:
        raise ValueError(f"候選配額或 workId 不正確：counts={counts}, workIds={work_ids}")
    return candidates


def repair_orphan_reservations(spec: CategorySpec, rows: list[dict]) -> None:
    manifest_path = ROOT / "data.json"
    manifest = findbook_writer.read_json(manifest_path)
    indexed_ids = {book.get("id") for book in manifest.get("books", [])}
    indexed_keys = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
    }
    candidate_keys = {
        findbook_writer.normalized_key(row["title"], row["author"])
        for row in rows
    }
    category_dir = ROOT / "Books" / spec.category_id
    for path in sorted(category_dir.glob("*.json")):
        book = findbook_writer.read_json(path)
        if book.get("workId") != WORK_ID or book.get("id") in indexed_ids:
            continue
        key = findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        if key not in candidate_keys:
            raise RuntimeError(f"孤兒 reservation 不在候選清單：{path.name}")
        if key in indexed_keys:
            raise RuntimeError(f"孤兒 reservation 與索引重複：{path.name}")
        if book.get("categoryId") != spec.category_id:
            raise RuntimeError(f"孤兒 reservation 分類不符：{path.name}")
        manifest["books"].append(findbook_writer.manifest_payload(book, spec.category_id))
        findbook_writer.update_manifest_metadata(manifest, FROM_DATE, TO_DATE)
        findbook_writer.write_json_atomic(manifest_path, manifest)
        verified = findbook_writer.read_json(manifest_path)
        if sum(item.get("id") == book.get("id") for item in verified.get("books", [])) != 1:
            raise RuntimeError(f"孤兒 reservation 索引修復驗證失敗：{path.name}")
        manifest = verified
        indexed_ids.add(book.get("id"))
        indexed_keys.add(key)
        print(f"reservation-repaired\t{spec.category_id}\t{book.get('id')}")


def reserve_and_complete(spec: CategorySpec, candidates: list[dict]) -> None:
    rows = [row for row in candidates if row["categoryId"] == spec.category_id]
    repair_orphan_reservations(spec, rows)
    manifest = findbook_writer.read_json(ROOT / "data.json")
    existing_keys = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
        if book.get("categoryId") == spec.category_id and book.get("workId") == WORK_ID
    }
    missing_rows = [
        row for row in rows
        if findbook_writer.normalized_key(row["title"], row["author"]) not in existing_keys
    ]
    if missing_rows:
        candidate_path = ROOT / "tools" / f".findbook_candidates_{spec.category_id[:2]}_20260715_{BATCH_NAME}.json"
        findbook_writer.write_json_atomic(candidate_path, missing_rows)
        findbook_writer.reserve(argparse.Namespace(
            root=ROOT,
            category_id=spec.category_id,
            category_file=None,
            candidates=candidate_path,
            limit=len(missing_rows),
            from_date=FROM_DATE,
            to_date=TO_DATE,
        ))
    else:
        print(f"reservation-already-complete\t{spec.category_id}\t{len(rows)}")
    manifest = findbook_writer.read_json(ROOT / "data.json")
    by_key = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", "")): book
        for book in manifest.get("books", [])
        if book.get("categoryId") == spec.category_id and book.get("workId") == WORK_ID
    }
    results = []
    for row in rows:
        key = findbook_writer.normalized_key(row["title"], row["author"])
        book = by_key.get(key)
        if book is None:
            raise RuntimeError(f"{row['title']} reservation 後找不到 workId 索引")
        detail = findbook_writer.read_json(ROOT / book["file"])
        if detail.get("chatgptStatus") == "complete":
            findbook_writer.validate_highlights(book["id"], detail.get("chatgptHighlights"))
            continue
        results.append({"id": book["id"], "highlights": highlight_source.highlights_for(row, spec.label)})
    if results:
        result_path = ROOT / "tools" / f".findbook_results_{spec.category_id[:2]}_20260715_{BATCH_NAME}.json"
        findbook_writer.write_json_atomic(result_path, results)
        findbook_writer.complete(argparse.Namespace(
            root=ROOT,
            category_id=spec.category_id,
            category_file=None,
            results=result_path,
        ))
    print(f"category-complete\t{spec.category_id}\t{len(results)}")


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
        f"FindBook_Skill.md fresh Codex-only {BATCH_NAME} 30/30/10/2/2/2/2 complete: "
        f"workId={WORK_ID} complete={complete} pending={pending}"
    )
    findbook_writer.write_json_atomic(ROOT / "data.json", manifest)


def main() -> None:
    parser = argparse.ArgumentParser(description=f"2026-07-15 FindBook {BATCH_NAME} 新書")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    if MASTER_CANDIDATES.exists() and not args.refresh:
        candidates = load_and_validate_candidates()
    else:
        candidates = prepare_candidates()
    if args.prepare_only or args.check_only:
        for spec in CATEGORIES:
            rows = [row for row in candidates if row["categoryId"] == spec.category_id]
            print(f"checked\t{spec.category_id}\t{len(rows)}")
        return
    for spec in CATEGORIES:
        reserve_and_complete(spec, candidates)
    update_manifest()
    print(f"fresh-{BATCH_NAME}-complete\tworkId={WORK_ID}\tbooks={len(candidates)}")


if __name__ == "__main__":
    main()
