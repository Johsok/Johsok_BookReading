from __future__ import annotations

import argparse
from pathlib import Path

import findbook_batch_20260714 as prior_batch
import findbook_writer


ROOT = Path(__file__).resolve().parents[1]
FROM_DATE = "2000-06-01"
TO_DATE = "2026-07-15"

CATEGORIES = (
    ("01_business_startup", "商業理財", 30, ROOT / "tools" / ".findbook_candidates_01_20260715.json"),
    ("02_psychology_growth", "心理勵志", 30, ROOT / "tools" / ".findbook_candidates_02_20260715.json"),
    ("03_natural_science", "自然科學", 10, ROOT / "tools" / ".findbook_candidates_03_07_20260715.json"),
    ("04_healthcare", "醫療保健", 2, ROOT / "tools" / ".findbook_candidates_03_07_20260715.json"),
    ("05_food_wellness", "飲食養生", 2, ROOT / "tools" / ".findbook_candidates_03_07_20260715.json"),
    ("06_computer_info", "電腦資訊", 2, ROOT / "tools" / ".findbook_candidates_03_07_20260715.json"),
    ("07_other", "其他", 2, ROOT / "tools" / ".findbook_candidates_03_07_20260715.json"),
)


def selected_candidates(category_id: str, quota: int, path: Path) -> list[dict]:
    rows = findbook_writer.read_json(path)
    if not isinstance(rows, list):
        raise ValueError(f"{path.name} 必須是 JSON 陣列")
    category_rows = [
        row for row in rows
        if row.get("categoryId", category_id) == category_id
        and not any(marker in str(row.get("title", "")) for marker in ("套書", "套組", "書+"))
    ]
    if len(category_rows) < quota:
        raise ValueError(f"{category_id} 只有 {len(category_rows)} 本候選，未達 {quota} 本")
    return category_rows[:quota]


def preflight() -> list[tuple[str, str, int, Path, list[dict]]]:
    manifest = findbook_writer.read_json(ROOT / "data.json")
    marker = f"-{TO_DATE.replace('-', '')}-"
    if any(marker in str(book.get("id", "")) for book in manifest.get("books", [])):
        raise RuntimeError("本日批次已存在，請先使用 queue/validate 續跑，不得重複附加")

    keys = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", ""))
        for book in manifest.get("books", [])
    }
    prepared = []
    duplicates = []
    for category_id, label, quota, path in CATEGORIES:
        rows = selected_candidates(category_id, quota, path)
        for row in rows:
            key = findbook_writer.normalized_key(row.get("title", ""), row.get("author", ""))
            if key in keys:
                duplicates.append(f"{label}\t{row.get('title')}\t{row.get('author')}")
            keys.add(key)
        prepared.append((category_id, label, quota, path, rows))
        print(f"candidate-ready\t{category_id}\t{len(rows)}")
    if duplicates:
        raise ValueError("候選與既有書庫或本批次重複：\n" + "\n".join(duplicates))
    print(f"preflight-valid\tbooks={sum(item[2] for item in prepared)}")
    return prepared


def reserve_and_complete(category_id: str, label: str, quota: int, path: Path, rows: list[dict]) -> None:
    selected_path = ROOT / "tools" / f".findbook_candidates_{category_id[:2]}_20260715.json"
    findbook_writer.write_json_atomic(selected_path, rows)
    findbook_writer.reserve(argparse.Namespace(
        root=ROOT,
        category_id=category_id,
        category_file=None,
        candidates=selected_path,
        limit=quota,
        from_date=FROM_DATE,
        to_date=TO_DATE,
    ))

    manifest = findbook_writer.read_json(ROOT / "data.json")
    by_key = {
        findbook_writer.normalized_key(book.get("title", ""), book.get("author", "")): book
        for book in manifest.get("books", [])
        if book.get("categoryId") == category_id
    }
    results = []
    for row in rows:
        key = findbook_writer.normalized_key(row["title"], row["author"])
        book = by_key.get(key)
        if book is None:
            raise RuntimeError(f"{row['title']} reservation 後找不到索引")
        highlight_row = dict(row)
        highlight_row["subjects"] = [tag for tag in row.get("tags", []) if tag != label]
        results.append({"id": book["id"], "highlights": prior_batch.highlights_for(highlight_row, label)})

    result_path = ROOT / "tools" / f".findbook_results_{category_id[:2]}_20260715.json"
    findbook_writer.write_json_atomic(result_path, results)
    findbook_writer.complete(argparse.Namespace(
        root=ROOT,
        category_id=category_id,
        category_file=None,
        results=result_path,
    ))
    print(f"category-complete\t{category_id}\t{len(results)}")


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
        "FindBook_Skill.md fresh Codex-only 30/30/10/2/2/2/2 batch complete: "
        f"complete={complete} pending={pending}"
    )
    findbook_writer.write_json_atomic(ROOT / "data.json", manifest)


def main() -> None:
    parser = argparse.ArgumentParser(description="2026-07-15 FindBook 新書批次")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    prepared = preflight()
    if args.check_only:
        return
    for item in prepared:
        reserve_and_complete(*item)
    update_manifest()
    print("fresh-batch-complete\tbooks=78")


if __name__ == "__main__":
    main()
