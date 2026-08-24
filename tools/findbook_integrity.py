# -*- coding: utf-8 -*-
"""Stable snapshot checks for data.json ↔ Books JSON links."""
from __future__ import annotations

import time
from collections import Counter
from pathlib import Path

import findbook_writer as writer


def _fingerprint(root: Path) -> tuple[str, float, int]:
    path = root / "data.json"
    manifest = writer.read_json(path)
    generated = str(manifest.get("generatedAt") or "")
    mtime = path.stat().st_mtime
    count = len(manifest.get("books") or [])
    return generated, mtime, count


def wait_until_stable(root: Path, retries: int = 3, pause: float = 0.4) -> None:
    root = Path(root).resolve()
    previous = _fingerprint(root)
    for _ in range(retries):
        time.sleep(pause)
        current = _fingerprint(root)
        if current == previous:
            return
        previous = current
    raise RuntimeError("data.json 仍在變動，無法取得穩定快照")


def check_snapshot(root: Path) -> dict:
    """Index-link integrity only. Does not inspect highlight wording."""
    root = Path(root).resolve()
    wait_until_stable(root)
    first = _fingerprint(root)
    manifest = writer.read_json(root / "data.json")
    books = manifest.get("books") or []
    errors: list[str] = []
    warnings: list[str] = []

    total = manifest.get("totalBooks")
    if total != len(books):
        errors.append(f"totalBooks {total} != len(books) {len(books)}")

    ids = [str(item.get("id") or "") for item in books]
    files = [str(item.get("file") or "").replace("\\", "/") for item in books]
    dup_ids = [key for key, count in Counter(ids).items() if key and count > 1]
    dup_files = [key for key, count in Counter(files).items() if key and count > 1]
    if dup_ids:
        errors.append(f"重複 id：{', '.join(dup_ids[:8])}")
    if dup_files:
        errors.append(f"重複 file：{', '.join(dup_files[:8])}")

    indexed = set(files)
    disk_books = []
    for path in (root / "Books").rglob("*.json"):
        relative = path.relative_to(root).as_posix()
        if path.name.startswith("_"):
            warnings.append(f"忽略暫存檔 {relative}")
            continue
        disk_books.append(relative)
    extra = sorted(set(disk_books) - indexed)
    missing = sorted(indexed - set(disk_books))
    if extra:
        errors.append(f"未入索引的單書檔 {len(extra)} 個，例如 {', '.join(extra[:5])}")
    if missing:
        errors.append(f"索引指向不存在的檔案 {len(missing)} 個，例如 {', '.join(missing[:5])}")
    if len(disk_books) != len(books):
        errors.append(f"磁碟單書 {len(disk_books)} != 索引 {len(books)}")

    for item in books:
        book_id = str(item.get("id") or "")
        category_id = str(item.get("categoryId") or "")
        relative_file = str(item.get("file") or "").replace("\\", "/")
        expected = writer.book_relative_path(category_id, book_id)
        if relative_file != expected:
            errors.append(f"{book_id} file {relative_file} != {expected}")
            continue
        path = root / relative_file
        if not path.is_file():
            continue
        try:
            book = writer.read_json(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{book_id} JSON 無法解析：{exc}")
            continue
        for field in ("id", "categoryId", "title", "author"):
            if book.get(field) != item.get(field):
                errors.append(f"{book_id} 欄位 {field} 與索引不一致")

    second = _fingerprint(root)
    if second != first:
        raise RuntimeError("檢查期間 data.json 又被寫入，請重跑穩定快照")

    return {
        "ok": not errors,
        "totalBooks": total,
        "indexCount": len(books),
        "diskCount": len(disk_books),
        "errors": errors,
        "warnings": warnings,
        "generatedAt": first[0],
    }
