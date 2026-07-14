from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PUNCT_RE = re.compile(r"[\s\W_]+", re.UNICODE)
NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
TAIPEI = ZoneInfo("Asia/Taipei")


def read_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json_atomic(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        json.loads(temp_path.read_text(encoding="utf-8"))
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def normalized_key(title: str, author: str) -> str:
    value = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT_RE.sub("", value)


def now_iso() -> str:
    return datetime.now(TAIPEI).isoformat(timespec="seconds")


def candidate_payload(candidate: dict, book_id: str, from_date: str, to_date: str) -> dict:
    required = ("title", "author", "sourceName", "sourceUrl", "sourceDateNote", "tags", "summary")
    missing = [field for field in required if not candidate.get(field)]
    if missing:
        raise ValueError(f"候選缺少欄位：{', '.join(missing)}")
    if not isinstance(candidate["tags"], list):
        raise ValueError(f"{candidate['title']} 的 tags 不是陣列")
    return {
        "id": book_id,
        "title": str(candidate["title"]).strip(),
        "author": str(candidate["author"]).strip(),
        "sourceName": str(candidate["sourceName"]).strip(),
        "sourceUrl": str(candidate["sourceUrl"]).strip(),
        "sourceDateNote": str(candidate["sourceDateNote"]).strip(),
        "searchDateRange": {"from": from_date, "to": to_date},
        "tags": [str(tag).strip() for tag in candidate["tags"] if str(tag).strip()],
        "summary": str(candidate["summary"]).strip(),
        "updatedAt": to_date,
        "chatgptHighlights": [],
        "chatgptStatus": "pending_codex",
        "highlightsSource": "pending_codex",
    }


def book_relative_path(category_id: str, book_id: str) -> str:
    return f"Books/{category_id}/{book_id}.json"


def manifest_payload(book: dict, category_id: str) -> dict:
    return {
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "categoryId": category_id,
        "tags": book["tags"],
        "sourceName": book["sourceName"],
        "sourceUrl": book["sourceUrl"],
        "file": book_relative_path(category_id, book["id"]),
    }


def resolve_category_id(args: argparse.Namespace, manifest: dict) -> str:
    category_id = str(getattr(args, "category_id", "") or "").strip()
    legacy_file = str(getattr(args, "category_file", "") or "").strip()
    if not category_id and legacy_file:
        category_id = Path(legacy_file).stem
    valid_ids = {str(item.get("id", "")) for item in manifest.get("categories", [])}
    if category_id not in valid_ids:
        raise ValueError(f"未知主題 categoryId：{category_id or '(空白)'}")
    return category_id


def allocate_id(category_id: str, to_date: str, ids: set[str]) -> str:
    base = f"{category_id}-{to_date.replace('-', '')}-"
    suffixes = []
    for book_id in ids:
        if not book_id.startswith(base):
            continue
        tail = book_id[len(base) :]
        if tail.isdigit():
            suffixes.append(int(tail))
    return f"{base}{max(suffixes, default=0) + 1:02d}"


def update_manifest_metadata(manifest: dict, from_date: str, to_date: str) -> None:
    books = manifest.get("books", [])
    manifest["totalBooks"] = len(books)
    manifest["searchDateRange"] = {"from": from_date, "to": to_date}
    manifest["generatedAt"] = now_iso()
    manifest["generatedFrom"] = "FindBook_Skill.md reservation checkpoint"


def reserve(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    manifest_path = root / "data.json"
    candidates = read_json(Path(args.candidates).resolve())
    if not isinstance(candidates, list):
        raise ValueError("candidates 必須是 JSON 陣列")

    committed = []
    skipped = []
    for candidate in candidates:
        if len(committed) >= args.limit:
            break
        manifest = read_json(manifest_path)
        category_id = resolve_category_id(args, manifest)
        manifest_books = manifest.get("books", [])
        key = normalized_key(str(candidate.get("title", "")), str(candidate.get("author", "")))
        existing_keys = {
            normalized_key(str(book.get("title", "")), str(book.get("author", "")))
            for book in manifest_books
        }
        if key in existing_keys:
            skipped.append(str(candidate.get("title", "")))
            continue

        book_directory = root / "Books" / category_id
        all_ids = {str(book.get("id", "")) for book in manifest_books}
        if book_directory.exists():
            all_ids.update(path.stem for path in book_directory.glob("*.json"))
        book_id = allocate_id(category_id, args.to_date, all_ids)
        book = candidate_payload(candidate, book_id, args.from_date, args.to_date)
        book["categoryId"] = category_id
        book_path = root / book_relative_path(category_id, book_id)

        write_json_atomic(book_path, book)
        check_book = read_json(book_path)
        if check_book.get("id") != book_id or check_book.get("categoryId") != category_id:
            raise RuntimeError(f"{book_id} 單書 pending 骨架寫後驗證失敗")

        manifest = read_json(manifest_path)
        latest_keys = {
            normalized_key(str(item.get("title", "")), str(item.get("author", "")))
            for item in manifest.get("books", [])
        }
        if key in latest_keys:
            raise RuntimeError(f"{book_id} 單書檔已寫入，但 data.json 出現 reservation 衝突")
        manifest.setdefault("books", []).append(manifest_payload(book, category_id))
        update_manifest_metadata(manifest, args.from_date, args.to_date)
        write_json_atomic(manifest_path, manifest)
        check_manifest = read_json(manifest_path)
        if sum(item.get("id") == book_id for item in check_manifest.get("books", [])) != 1:
            raise RuntimeError(f"{book_id} data.json 寫後驗證失敗")
        committed.append(book_id)
        print(f"committed\t{book_id}")

    print(f"committed={len(committed)} skipped={len(skipped)} requested={args.limit}")
    if len(committed) != args.limit:
        raise RuntimeError(f"合格新書只有 {len(committed)} 本，未達 {args.limit} 本")
    return 0


def validate_highlights(book_id: str, highlights: object) -> list[str]:
    if not isinstance(highlights, list) or len(highlights) != 150:
        raise ValueError(f"{book_id} 必須剛好 150 點")
    short_colon_lines = []
    cleaned = []
    for index, line in enumerate(highlights, 1):
        expected = f"{index:03d}、"
        if not isinstance(line, str) or not line.startswith(expected):
            raise ValueError(f"{book_id} 第 {index} 點編號錯誤")
        if "\n" in line or "\r" in line or "｜" in line:
            raise ValueError(f"{book_id} 第 {index} 點含禁用格式")
        body = NUMBER_RE.sub("", line, count=1).strip()
        if not body:
            raise ValueError(f"{book_id} 第 {index} 點沒有正文")
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
            short_colon_lines.append(index)
        cleaned.append(line.strip())
    if len(short_colon_lines) >= 3:
        raise ValueError(f"{book_id} 有 {len(short_colon_lines)} 點疑似短標籤加冒號")
    return cleaned


def complete(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    manifest_path = root / "data.json"
    results = read_json(Path(args.results).resolve())
    if isinstance(results, dict):
        results = [results]
    if not isinstance(results, list):
        raise ValueError("results 必須是 JSON 物件或陣列")

    for result in results:
        book_id = str(result.get("id", ""))
        highlights = validate_highlights(book_id, result.get("highlights"))
        manifest = read_json(manifest_path)
        matches = [book for book in manifest.get("books", []) if book.get("id") == book_id]
        if len(matches) != 1:
            raise ValueError(f"{book_id} 在 data.json 必須剛好出現一次")
        index_book = matches[0]
        expected_category_id = resolve_category_id(args, manifest) if (
            getattr(args, "category_id", None) or getattr(args, "category_file", None)
        ) else str(index_book.get("categoryId", ""))
        if index_book.get("categoryId") != expected_category_id:
            raise ValueError(f"{book_id} 不屬於 {expected_category_id}")
        relative_file = str(index_book.get("file", ""))
        expected_file = book_relative_path(expected_category_id, book_id)
        if relative_file != expected_file:
            raise ValueError(f"{book_id} 的 data.json file 必須是 {expected_file}")
        book_path = root / relative_file
        book = read_json(book_path)
        if book.get("id") != book_id:
            raise ValueError(f"{book_id} 單書檔 ID 不一致")
        book["chatgptHighlights"] = highlights
        book["chatgptStatus"] = "complete"
        book["highlightsSource"] = "codex"
        book["highlightsCapturedAt"] = now_iso()
        book["updatedAt"] = datetime.now(TAIPEI).date().isoformat()
        write_json_atomic(book_path, book)

        saved = read_json(book_path)
        if saved.get("id") != book_id:
            raise RuntimeError(f"{book_id} 寫後找不到")
        validate_highlights(book_id, saved.get("chatgptHighlights"))
        if saved.get("chatgptStatus") != "complete":
            raise RuntimeError(f"{book_id} 寫後狀態不是 complete")
        print(f"written\t{book_id}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FindBook reservation 與 Codex 結果單一 writer")
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1])
    subparsers = parser.add_subparsers(dest="command", required=True)

    reserve_parser = subparsers.add_parser("reserve")
    reserve_category = reserve_parser.add_mutually_exclusive_group(required=True)
    reserve_category.add_argument("--category-id")
    reserve_category.add_argument("--category-file", help="舊參數相容；只用檔名推導 categoryId，不讀寫分類檔")
    reserve_parser.add_argument("--candidates", required=True)
    reserve_parser.add_argument("--limit", type=int, required=True)
    reserve_parser.add_argument("--from-date", required=True)
    reserve_parser.add_argument("--to-date", required=True)
    reserve_parser.set_defaults(func=reserve)

    complete_parser = subparsers.add_parser("complete")
    complete_category = complete_parser.add_mutually_exclusive_group()
    complete_category.add_argument("--category-id")
    complete_category.add_argument("--category-file", help="舊參數相容；只用檔名驗證 categoryId，不讀寫分類檔")
    complete_parser.add_argument("--results", required=True)
    complete_parser.set_defaults(func=complete)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
