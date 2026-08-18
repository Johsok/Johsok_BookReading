# -*- coding: utf-8 -*-
"""Extract Grok highlights from transcripts and write book JSON without content QA."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import findbook_writer as writer

ROOT = Path(__file__).resolve().parents[1]
TAIPEI = ZoneInfo("Asia/Taipei")
TRANSCRIPT_DIR = Path(
    r"C:\Users\johso\.cursor\projects\c-Users-johso-OneDrive-Desktop-Johsok-BookReading"
    r"\agent-transcripts\07cf68a5-fdfe-48c6-bea0-024782ef6a1c\subagents"
)
LINE_RE = re.compile(r"^(\d{3})、")
BOOK_MAP = {
    "50d9b174-debc-4da6-bb00-532b1e51e423": "01_business_startup-20260818-08",
    "c28f6bd6-eb2b-41b5-9103-77be458bf11f": "01_business_startup-20260818-09",
    "5d841e20-db61-467b-9183-ad6751b263eb": "01_business_startup-20260818-10",
    "6fcb645f-f8bb-4258-82a8-cde673aa387e": "01_business_startup-20260818-11",
    "34327514-cda5-40ea-8b27-fff69dac8d20": "01_business_startup-20260818-12",
    "dd9b0c59-db7b-4ac5-ab95-654f484adac4": "02_psychology_growth-20260818-08",
    "780be28e-e0e5-4281-a711-cbf626a29a01": "02_psychology_growth-20260818-09",
    "23d61ab8-749b-4630-ab12-01957d5b723a": "02_psychology_growth-20260818-10",
    "9fc11243-e351-4c27-81b8-94e15d99e107": "02_psychology_growth-20260818-11",
    "887797a1-d936-4159-bbe4-57adb2904bf6": "02_psychology_growth-20260818-12",
}


def extract_highlights(path: Path) -> list[str]:
    collected: dict[int, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        message = event.get("message") or {}
        for block in message.get("content") or []:
            if not isinstance(block, dict) or block.get("type") != "text":
                continue
            text = str(block.get("text") or "")
            if "001、" not in text:
                continue
            for line in text.splitlines():
                stripped = line.strip()
                match = LINE_RE.match(stripped)
                if not match:
                    continue
                collected[int(match.group(1))] = stripped
    missing = [index for index in range(1, 151) if index not in collected]
    if missing:
        raise SystemExit(f"{path.name} missing {len(missing)} lines, first={missing[:8]}")
    return [collected[index] for index in range(1, 151)]


def check_index_link(manifest: dict, index_book: dict, book: dict) -> None:
    book_id = str(index_book.get("id", ""))
    category_id = str(index_book.get("categoryId", ""))
    expected_file = f"Books/{category_id}/{book_id}.json"
    if str(index_book.get("file", "")) != expected_file:
        raise SystemExit(f"{book_id} file path mismatch")
    for field in ("id", "categoryId", "title", "author"):
        if index_book.get(field) != book.get(field):
            raise SystemExit(f"{book_id} {field} mismatch with index")


def check_stable_snapshot() -> None:
    manifest_path = ROOT / "data.json"
    first_mtime = manifest_path.stat().st_mtime
    first_generated = writer.read_json(manifest_path).get("generatedAt")
    first_count = len(writer.read_json(manifest_path).get("books", []))
    manifest = writer.read_json(manifest_path)
    if (
        manifest_path.stat().st_mtime != first_mtime
        or manifest.get("generatedAt") != first_generated
        or len(manifest.get("books", [])) != first_count
    ):
        raise SystemExit("snapshot moved during check")
    books = manifest.get("books", [])
    if manifest.get("totalBooks") != len(books):
        raise SystemExit(f"totalBooks={manifest.get('totalBooks')} books={len(books)}")
    ids = [book.get("id") for book in books]
    files = [book.get("file") for book in books]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate id in data.json")
    if len(files) != len(set(files)):
        raise SystemExit("duplicate file in data.json")
    disk_files = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.glob("Books/**/*.json"))
    indexed_files = sorted(str(path) for path in files)
    if disk_files != indexed_files:
        extra = sorted(set(disk_files) - set(indexed_files))
        missing = sorted(set(indexed_files) - set(disk_files))
        raise SystemExit(f"book files mismatch extra={extra[:5]} missing={missing[:5]}")
    for index_book in books:
        relative_file = str(index_book.get("file", ""))
        book = writer.read_json(ROOT / relative_file)
        check_index_link(manifest, index_book, book)
    print(f"index-ok\ttotalBooks={len(books)}")


def main() -> None:
    written = []
    for agent_id, book_id in BOOK_MAP.items():
        highlights = extract_highlights(TRANSCRIPT_DIR / f"{agent_id}.jsonl")
        manifest = writer.read_json(ROOT / "data.json")
        matches = [book for book in manifest.get("books", []) if book.get("id") == book_id]
        if len(matches) != 1:
            raise SystemExit(f"{book_id} must appear once in data.json")
        relative_file = str(matches[0]["file"])
        book_path = ROOT / relative_file
        book = writer.read_json(book_path)
        check_index_link(manifest, matches[0], book)
        book["chatgptHighlights"] = highlights
        book["chatgptStatus"] = "complete"
        book["highlightsSource"] = "grok"
        book["highlightsCapturedAt"] = datetime.now(TAIPEI).isoformat(timespec="seconds")
        book["updatedAt"] = datetime.now(TAIPEI).date().isoformat()
        writer.write_json_atomic(book_path, book)
        saved = writer.read_json(book_path)
        if saved.get("id") != book_id:
            raise SystemExit(f"{book_id} write failed")
        check_index_link(writer.read_json(ROOT / "data.json"), matches[0], saved)
        print(f"written\t{book_id}\t{len(saved.get('chatgptHighlights', []))}")
        written.append(book_id)
    check_stable_snapshot()
    print("done\t" + ",".join(written))


if __name__ == "__main__":
    main()
