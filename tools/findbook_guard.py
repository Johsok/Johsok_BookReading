from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


CATEGORY_IDS = (
    "01_business_startup",
    "02_psychology_growth",
    "03_natural_science",
    "04_healthcare",
    "05_food_wellness",
    "06_computer_info",
    "07_other",
)
NUMBER_RE = re.compile(r"^\d{2,3}、")
PRIVATE_RE = re.compile(r"[\ue000-\uf8ff\ufffd]")
PROMO_BRACKET_RE = re.compile(r"【[^】]*】|\[[^\]]*\]")
PROMO_WORD_RE = re.compile(
    r"(?:珍藏|紀念|暢銷|旅行特別|作者親簽|限量|首刷|博客來獨家|長銷慶功)版|"
    r"(?:隨書|附贈|贈送)[^：:，,。]*"
)
PUNCT_RE = re.compile(r"[\s\W_]+", re.UNICODE)
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalized_key(title: str, author: str) -> str:
    text = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT_RE.sub("", text)


def canonical_title(title: str) -> str:
    text = unicodedata.normalize("NFKC", title).casefold()
    text = PROMO_BRACKET_RE.sub("", text)
    text = PROMO_WORD_RE.sub("", text)
    return PUNCT_RE.sub("", text)


def parse_expected(value: str | None) -> list[int] | None:
    if value is None:
        return None
    values = [int(item.strip()) for item in value.split(",")]
    if len(values) != len(CATEGORY_IDS):
        raise argparse.ArgumentTypeError("--expected-new 必須提供 7 個逗號分隔數字")
    return values


def read_baseline_ids(root: Path, filename: str, baseline_ref: str) -> set[str] | None:
    result = subprocess.run(
        ["git", "show", f"{baseline_ref}:{filename}"],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        parsed = json.loads(result.stdout.lstrip("\ufeff"))
    except json.JSONDecodeError:
        return None
    return {book["id"] for book in parsed.get("books", [])}


def validate_highlights(book: dict, errors: list[str]) -> None:
    status = book.get("chatgptStatus")
    lines = book.get("chatgptHighlights")
    if not isinstance(lines, list):
        errors.append(f"{book.get('id')} chatgptHighlights 不是陣列")
        return
    if status != "complete":
        return
    if len(lines) not in (100, 150, 200):
        errors.append(f"{book.get('id')} Codex 完成狀態卻不是相容的 100、150 或 200 點")
        return
    if len(lines) in (150, 200):
        if book.get("highlightsSource") != "codex":
            errors.append(f"{book.get('id')} 新版 Codex 重點的 highlightsSource 必須是 codex")
        if not book.get("highlightsCapturedAt"):
            errors.append(f"{book.get('id')} 新版 Codex 重點缺少 highlightsCapturedAt")
    number_width = 3 if len(lines) in (150, 200) else 2
    short_colon_lines = []
    for index, line in enumerate(lines, 1):
        expected = f"{index:0{number_width}d}、"
        if not isinstance(line, str) or not line.startswith(expected):
            errors.append(f"{book.get('id')} Codex 第 {index} 點編號錯誤")
            continue
        if "\n" in line or "\r" in line or "｜" in line:
            errors.append(f"{book.get('id')} Codex 第 {index} 點含禁用格式")
        body = NUMBER_RE.sub("", line, count=1)
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
            short_colon_lines.append(index)
    if len(short_colon_lines) >= 3:
        errors.append(
            f"{book.get('id')} Codex 有 {len(short_colon_lines)} 點疑似短標籤加冒號"
        )


def load_catalog(root: Path) -> tuple[list[dict], dict[str, dict], dict]:
    manifest = read_json(root / "data.json")
    categories = [
        {"categoryId": category_id, "books": []}
        for category_id in CATEGORY_IDS
    ]
    category_map = {category["categoryId"]: category for category in categories}
    details = {}
    for item in manifest.get("books", []):
        book_id = str(item.get("id", ""))
        category_id = str(item.get("categoryId", ""))
        relative_file = str(item.get("file", ""))
        if category_id not in category_map:
            raise ValueError(f"{book_id} 使用未知主題：{category_id}")
        if not relative_file:
            raise ValueError(f"{book_id} 的 data.json 索引缺少 file")
        detail_path = (root / relative_file).resolve()
        try:
            detail_path.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"{book_id} 的 file 超出專案目錄") from exc
        detail = read_json(detail_path)
        copy = dict(detail)
        copy["_filename"] = relative_file
        details[book_id] = copy
        category_map[category_id]["books"].append(copy)
    return categories, details, manifest


def run_validate(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    try:
        categories, details, manifest = load_catalog(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR JSON 解析失敗：{exc}")
        return 1

    detail_books = list(details.values())
    if len(details) != sum(len(category.get("books", [])) for category in categories):
        errors.append("單書索引含重複 ID")
    if manifest.get("totalBooks") != len(manifest.get("books", [])):
        errors.append("data.json totalBooks 與 books 數量不一致")
    if len(manifest.get("books", [])) != len(detail_books):
        errors.append("data.json 與單書檔總數不一致")

    manifest_ids = set()
    indexed_files = set()
    for item in manifest.get("books", []):
        book_id = item.get("id")
        if book_id in manifest_ids:
            errors.append(f"data.json 重複 ID：{book_id}")
        manifest_ids.add(book_id)
        detail = details.get(book_id)
        if detail is None:
            errors.append(f"data.json 找不到分類明細：{book_id}")
            continue
        expected_file = f"Books/{item.get('categoryId')}/{book_id}.json"
        if item.get("file") != expected_file:
            errors.append(f"{book_id} file 路徑應為 {expected_file}")
        indexed_files.add(str(item.get("file", "")))
        checks = (
            ("title", item.get("title"), detail.get("title")),
            ("author", item.get("author"), detail.get("author")),
            ("categoryId", item.get("categoryId"), detail.get("categoryId")),
            ("tags", item.get("tags"), detail.get("tags")),
            ("sourceName", item.get("sourceName"), detail.get("sourceName")),
            ("sourceUrl", item.get("sourceUrl"), detail.get("sourceUrl")),
        )
        for field, left, right in checks:
            if left != right:
                errors.append(f"{book_id} manifest/detail {field} 不一致")

    actual_files = {
        path.relative_to(root).as_posix()
        for path in (root / "Books").glob("**/*.json")
    }
    for relative_file in sorted(actual_files - indexed_files):
        errors.append(f"Books 含未被 data.json 索引的單書檔：{relative_file}")
    for relative_file in sorted(indexed_files - actual_files):
        errors.append(f"data.json 指向不存在的單書檔：{relative_file}")

    keys: dict[str, list[str]] = defaultdict(list)
    semantic_keys: dict[tuple[str, str], list[str]] = defaultdict(list)
    for book in detail_books:
        title = str(book.get("title", ""))
        author = str(book.get("author", ""))
        keys[normalized_key(title, author)].append(book.get("id", ""))
        semantic_keys[(canonical_title(title), normalized_key("", author))].append(book.get("id", ""))
        if not title or not author:
            errors.append(f"{book.get('id')} 缺少書名或作者")
        if PRIVATE_RE.search(json.dumps(book, ensure_ascii=False)):
            errors.append(f"{book.get('id')} 含私用區或替代字元")
        date_range = book.get("searchDateRange") or {}
        if not date_range.get("from") or not date_range.get("to"):
            errors.append(f"{book.get('id')} 缺少 searchDateRange")
        if not book.get("sourceDateNote") or not book.get("sourceUrl"):
            errors.append(f"{book.get('id')} 缺少來源日期說明或網址")
        validate_highlights(book, errors)
        if "套書" in title or re.search(r"共[兩二三四五六七八九十\d]+冊", title):
            warnings.append(f"{book.get('id')} 是套書，需人工檢查是否重疊單冊")

    for ids in keys.values():
        if len(ids) > 1:
            errors.append(f"正規化 title+author 重複：{', '.join(ids)}")
    for ids in semantic_keys.values():
        if len(ids) > 1:
            warnings.append(f"疑似版本重複：{', '.join(ids)}")

    expected = parse_expected(args.expected_new)
    new_books: list[dict] = []
    deltas = []
    baseline_ids = read_baseline_ids(root, "data.json", args.baseline_ref)
    if baseline_ids is None:
        warnings.append(f"無法讀取 {args.baseline_ref}:data.json，略過新增配額檢查")
    for index, category in enumerate(categories):
        additions = [
            book
            for book in category.get("books", [])
            if baseline_ids is not None and book.get("id") not in baseline_ids
        ]
        new_books.extend(additions)
        deltas.append(len(additions))
        if expected is not None and len(additions) != expected[index]:
            errors.append(f"{category.get('categoryId')} 新增 {len(additions)} 本，預期 {expected[index]} 本")
    if args.from_date or args.to_date:
        for book in new_books:
            date_range = book.get("searchDateRange") or {}
            if args.from_date and date_range.get("from") != args.from_date:
                errors.append(f"{book.get('id')} 起始日期不符")
            if args.to_date and date_range.get("to") != args.to_date:
                errors.append(f"{book.get('id')} 結束日期不符")
    if expected is not None:
        for book in new_books:
            if book.get("chatgptStatus") != "complete":
                errors.append(f"{book.get('id')} 本次新增書籍的 Codex 重點尚未完成")
            elif len(book.get("chatgptHighlights") or []) != 150:
                errors.append(f"{book.get('id')} 本次新增書籍的 Codex 重點必須剛好 150 點")

    for category in categories:
        books = category.get("books", [])
        signatures = Counter(tuple(book.get("tags", [])) for book in books if book.get("id") in {item.get("id") for item in new_books})
        if signatures:
            signature, count = signatures.most_common(1)[0]
            if count >= 4 and count / max(1, sum(signatures.values())) >= 0.8:
                warnings.append(f"{category.get('categoryId')} 新書有 {count} 本共用相同 tags：{list(signature)}")

    template_summaries = [book.get("id") for book in detail_books if str(book.get("summary", "")).startswith("本書取自")]
    if template_summaries:
        warnings.append(f"仍有 {len(template_summaries)} 本使用流程模板 summary")

    complete = sum(book.get("chatgptStatus") == "complete" for book in detail_books)
    pending = len(detail_books) - complete
    generated_from = str(manifest.get("generatedFrom", ""))
    if generated_from and (str(complete) not in generated_from or str(pending) not in generated_from):
        warnings.append("data.json generatedFrom 仍是舊版完成／待處理統計")

    counts = [len(category.get("books", [])) for category in categories]
    print(f"分類總數：{'/'.join(map(str, counts))}")
    if deltas:
        print(f"相對 {args.baseline_ref} 新增：{'/'.join(map(str, deltas))}")
    print(f"全庫：{len(detail_books)} 本；complete={complete}；pending={pending}")
    for warning in sorted(set(warnings)):
        print(f"WARN {warning}")
    for error in sorted(set(errors)):
        print(f"ERROR {error}")
    print("VALID" if not errors else "INVALID")
    return 0 if not errors else 1


def run_queue(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    try:
        categories, _, _ = load_catalog(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR JSON 解析失敗：{exc}")
        return 1
    rows = []
    for category in categories:
        for book in category.get("books", []):
            if book.get("chatgptStatus") != "complete":
                rows.append((category.get("categoryId"), "Codex", book))
    if args.limit is not None:
        rows = rows[: args.limit]
    for category_id, model, book in rows:
        print(f"{category_id}\t{model}\t{book.get('id')}\t{book.get('title')}\t{book.get('author')}")
    print(f"待處理模型工作：{len(rows)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FindBook JSON 唯讀預檢與驗證")
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1])
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--expected-new")
    validate.add_argument("--baseline-ref", default="HEAD")
    validate.add_argument("--from-date")
    validate.add_argument("--to-date")
    validate.set_defaults(func=run_validate)
    queue = subparsers.add_parser("queue")
    queue.add_argument("--limit", type=int)
    queue.set_defaults(func=run_queue)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
