# -*- coding: utf-8 -*-
"""Stable snapshot index-file integrity check for the 20260824 batch."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_IDS = [
    "01_business_startup-20260824-01",
    "01_business_startup-20260824-02",
    "01_business_startup-20260824-03",
    "01_business_startup-20260824-04",
    "01_business_startup-20260824-05",
    "02_psychology_growth-20260824-01",
    "02_psychology_growth-20260824-02",
    "02_psychology_growth-20260824-03",
    "02_psychology_growth-20260824-04",
    "02_psychology_growth-20260824-05",
    "03_natural_science-20260824-01",
    "03_natural_science-20260824-02",
    "03_natural_science-20260824-03",
    "03_natural_science-20260824-04",
    "03_natural_science-20260824-05",
]


def main() -> int:
    manifest_path = ROOT / "data.json"
    stat1 = manifest_path.stat()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    snap = {
        "generatedAt": manifest.get("generatedAt"),
        "n": len(manifest.get("books", [])),
        "total": manifest.get("totalBooks"),
        "mtime": stat1.st_mtime,
    }
    books = manifest.get("books", [])
    ok = True
    errs: list[str] = []
    if snap["total"] != snap["n"]:
        ok = False
        errs.append(f"totalBooks {snap['total']} != len {snap['n']}")
    id_seen: set[str] = set()
    file_seen: set[str] = set()
    for item in books:
        book_id = str(item.get("id") or "")
        relative = str(item.get("file") or "").replace("\\", "/")
        if book_id in id_seen:
            ok = False
            errs.append(f"dup id {book_id}")
        id_seen.add(book_id)
        if relative in file_seen:
            ok = False
            errs.append(f"dup file {relative}")
        file_seen.add(relative)
        path = ROOT / relative
        if not path.exists():
            ok = False
            errs.append(f"missing {relative}")
            continue
        book = json.loads(path.read_text(encoding="utf-8-sig"))
        if (
            book.get("id") != book_id
            or book.get("categoryId") != item.get("categoryId")
            or book.get("title") != item.get("title")
            or book.get("author") != item.get("author")
        ):
            ok = False
            errs.append(f"mismatch {book_id}")
    disk = sorted(p.resolve().as_posix() for p in (ROOT / "Books").rglob("*.json"))
    expected = sorted((ROOT / relative).resolve().as_posix() for relative in file_seen)
    if disk != expected:
        ok = False
        only_disk = set(disk) - set(expected)
        only_idx = set(expected) - set(disk)
        if only_disk:
            errs.append(f"unindexed json {len(only_disk)} e.g. {next(iter(only_disk))}")
        if only_idx:
            errs.append(f"index without file {len(only_idx)} e.g. {next(iter(only_idx))}")
    pending: list[str] = []
    for book_id in BATCH_IDS:
        hits = [item for item in books if item.get("id") == book_id]
        if len(hits) != 1:
            ok = False
            errs.append(f"batch id {book_id} hits={len(hits)}")
            continue
        book = json.loads((ROOT / hits[0]["file"]).read_text(encoding="utf-8-sig"))
        status = book.get("chatgptStatus")
        count = len(book.get("chatgptHighlights") or [])
        if status != "complete":
            pending.append(book_id)
        print(f"{book_id}\t{status}\t{count}")
    stat2 = manifest_path.stat()
    manifest2 = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    moved = (
        manifest2.get("generatedAt") != snap["generatedAt"]
        or len(manifest2.get("books", [])) != snap["n"]
        or manifest2.get("totalBooks") != snap["total"]
        or stat2.st_mtime != snap["mtime"]
    )
    print(f"snapshot {snap['generatedAt']} total {snap['total']}")
    print("moved" if moved else "stable")
    print("pending", pending or "none")
    print("FAIL" if not ok else "PASS")
    if errs:
        print("\n".join(errs[:20]))
    return 0 if ok and not moved and not pending else 1


if __name__ == "__main__":
    raise SystemExit(main())
