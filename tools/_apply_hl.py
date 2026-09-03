# -*- coding: utf-8 -*-
"""Ingest Grok highlight lines from this batch's subagent transcripts and write them."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from findbook_highlights import extract_highlights, write_highlights
from findbook_writer import read_json

ROOT = Path(__file__).resolve().parents[1]
LINE_RE = re.compile(r"^(\d{3})、")
GARBLE_MARKERS = (
    "\ufffd",
    "锟斤拷",
    "ï¿½",
    "&#x",
    "&amp;",
)
MOJIBAKE_RE = re.compile(r"[ÃÂåæç][\x80-\xff]|涓鍙鏌")
WORK_ID = "findbook-20260903-1119"
SUBAGENT_DIR = Path(
    r"C:\Users\johso\.cursor\projects\c-Users-johso-OneDrive-Desktop-Johsok-BookReading"
    r"\agent-transcripts\fb55188e-a6b0-47af-a32d-bee49b72b9ee\subagents"
)


def looks_garbled(text: str) -> bool:
    if any(marker in text for marker in GARBLE_MARKERS):
        return True
    if "\\u" in text and re.search(r"\\u[0-9a-fA-F]{4}", text):
        return True
    if MOJIBAKE_RE.search(text):
        return True
    return bool(re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", text))


def iter_texts(node) -> list[str]:
    texts: list[str] = []
    if isinstance(node, str):
        texts.append(node)
        return texts
    if isinstance(node, dict):
        if node.get("type") == "text" and isinstance(node.get("text"), str):
            texts.append(node["text"])
        for value in node.values():
            texts.extend(iter_texts(value))
        return texts
    if isinstance(node, list):
        for item in node:
            texts.extend(iter_texts(item))
    return texts


def collect_segments(path: Path) -> list[tuple[str, list[str]]]:
    title = ""
    segments: list[tuple[str, list[str]]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        obj = json.loads(raw)
        blob = "\n".join(iter_texts(obj))
        if not title:
            match = re.search(r"^書名：(.+)$", blob, re.M)
            if match:
                title = match.group(1).strip()
        found: dict[int, str] = {}
        for line in blob.splitlines():
            line = line.strip()
            match = LINE_RE.match(line)
            if not match:
                continue
            number = int(match.group(1))
            if 1 <= number <= 150:
                found[number] = line
        if found:
            segments.append((title, [found[index] for index in sorted(found)]))
    return segments


def main() -> int:
    manifest = read_json(ROOT / "data.json")
    title_to_id = {}
    for item in manifest.get("books", []):
        if item.get("id", "").endswith(tuple(f"-20240903-{n:02d}" for n in range(26, 31))):
            title_to_id[item["title"]] = item["id"]

    grouped: dict[str, dict[int, str]] = defaultdict(dict)
    for path in sorted(SUBAGENT_DIR.glob("*.jsonl")):
        for title, lines in collect_segments(path):
            if title not in title_to_id:
                continue
            for line in lines:
                number = int(line[:3])
                grouped[title][number] = line

    written = 0
    pending = []
    for title, book_id in sorted(title_to_id.items(), key=lambda item: item[1]):
        found = grouped.get(title) or {}
        highlights = [found[index] for index in range(1, 151) if index in found]
        missing = [index for index in range(1, 151) if index not in found]
        if missing:
            pending.append((book_id, title, missing[:8], len(missing)))
            continue
        blob = "\n".join(highlights)
        if looks_garbled(blob):
            raise SystemExit(f"garbled highlights blocked for {book_id}")
        cleaned = extract_highlights(blob)
        if len(cleaned) != 150:
            raise SystemExit(f"{book_id} extracted {len(cleaned)}")
        result = write_highlights(ROOT, book_id, cleaned)
        print(f"written\t{result['id']}\t{result['count']}")
        written += 1
    for book_id, title, sample, count in pending:
        print(f"pending\t{book_id}\tmissing={count}\te.g.{sample}\t{title[:24]}")
    print(f"done written={written} pending={len(pending)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
