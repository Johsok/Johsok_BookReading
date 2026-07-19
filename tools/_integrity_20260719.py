# -*- coding: utf-8 -*-
"""Index link integrity check for FindBook batch (no content validation)."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK_ID = "findbook-20260719-220407"


def main() -> int:
    manifest = json.loads((ROOT / "data.json").read_text(encoding="utf-8-sig"))
    books = manifest.get("books", [])
    errors = []
    if manifest.get("totalBooks") != len(books):
        errors.append(f"totalBooks mismatch: {manifest.get('totalBooks')} != {len(books)}")

    ids = [b.get("id") for b in books]
    files = [b.get("file") for b in books]
    id_counts = Counter(ids)
    file_counts = Counter(files)
    for book_id, count in id_counts.items():
        if count != 1:
            errors.append(f"duplicate id: {book_id} x{count}")
    for file_path, count in file_counts.items():
        if count != 1:
            errors.append(f"duplicate file: {file_path} x{count}")

    indexed_files = set()
    for book in books:
        book_id = book.get("id")
        category_id = book.get("categoryId")
        relative = book.get("file")
        expected = f"Books/{category_id}/{book_id}.json"
        if relative != expected:
            errors.append(f"{book_id} file path mismatch: {relative} != {expected}")
            continue
        path = ROOT / relative
        indexed_files.add(path.resolve())
        if not path.exists():
            errors.append(f"missing file: {relative}")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"unreadable {relative}: {exc}")
            continue
        for field in ("id", "categoryId", "title", "author"):
            if payload.get(field) != book.get(field):
                errors.append(f"{book_id} field mismatch: {field}")

    disk_files = {p.resolve() for p in (ROOT / "Books").rglob("*.json")}
    orphan = disk_files - indexed_files
    missing_on_disk = indexed_files - disk_files
    if orphan:
        errors.append(f"orphan book json count={len(orphan)}")
    if missing_on_disk:
        errors.append(f"indexed missing on disk count={len(missing_on_disk)}")
    if len(disk_files) != len(books):
        errors.append(f"disk json {len(disk_files)} != indexed {len(books)}")

    batch = [b for b in books if b.get("workId") == WORK_ID]
    complete = 0
    pending = 0
    for book in batch:
        path = ROOT / book["file"]
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        status = payload.get("chatgptStatus")
        if status == "complete" and payload.get("highlightsSource") == "grok":
            complete += 1
        else:
            pending += 1
            print(f"pending\t{book['id']}\t{status}")

    print(f"batch\tworkId={WORK_ID}\treserved={len(batch)}\tcomplete={complete}\tpending={pending}")
    print(f"integrity\terrors={len(errors)}")
    for err in errors[:30]:
        print(f"error\t{err}")
    return 0 if not errors and pending == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
