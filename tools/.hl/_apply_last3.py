# -*- coding: utf-8 -*-
"""Apply last3 FindBook highlight segments from current-session subagent transcripts."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_highlights import extract_highlights, write_highlights

BASE = Path(
    r"C:\Users\johso\.cursor\projects\c-Users-johso-OneDrive-Desktop-Johsok-BookReading"
    r"\agent-transcripts\25b0c464-8032-4132-ac3a-e304cd3c4595\subagents"
)
LINE = re.compile(r"^(\d{3})、")
MAP = {
    "863fd7b1-69e9-47da-ab23-3a19a619d715": ("05_food_wellness-20210913-16", 1),
    "cc7c6d1e-dce3-46bd-9263-d511b3dfbb47": ("05_food_wellness-20210913-16", 76),
    "33a96c54-fd26-46e5-9d87-841895a27d5e": ("05_food_wellness-20210913-17", 1),
    "020fd279-25da-485c-a06b-3f07eb39ae9d": ("05_food_wellness-20210913-17", 76),
    "18bcb7fd-5051-4f92-9968-e365b9c6d916": ("05_food_wellness-20210913-18", 1),
    "97a2b0d1-ace8-4f27-9833-910cf60a1ddc": ("05_food_wellness-20210913-18", 76),
    "973a8110-caee-4c4e-8750-e47932f6b59e": ("05_food_wellness-20210913-19", 1),
    "118e0606-510a-459e-bef7-ceeeb49c19d7": ("05_food_wellness-20210913-19", 76),
    "8473d10c-dc0a-474f-ba2f-af438c0dabcf": ("05_food_wellness-20210913-20", 1),
    "56f892c3-14f4-409e-b3e1-8ab715d9b107": ("05_food_wellness-20210913-20", 76),
    "fa7bd319-53ee-4c7e-9626-0e8a9854bfc3": ("06_computer_info-20210913-16", 1),
    "1b9456d5-d65a-4d46-9ced-54eebb6f6335": ("06_computer_info-20210913-16", 76),
    "d25ad53b-38ea-4f3a-bef3-2e904d54b44e": ("06_computer_info-20210913-17", 1),
    "a08ae00c-600d-4a55-8104-8c6d256e4a93": ("06_computer_info-20210913-17", 76),
    "d305d81c-1463-476c-9753-25e8217d55cf": ("06_computer_info-20210913-18", 1),
    "6ca128ab-dd1b-4c06-9350-51f74ed3f077": ("06_computer_info-20210913-18", 76),
    "2220681d-ab2a-42f9-995a-2978408bc53d": ("06_computer_info-20210913-19", 1),
    "1938f8d8-36cd-4456-8dfe-d43a89bacdba": ("06_computer_info-20210913-19", 76),
    "1a4c09fe-9b15-4201-9a3a-b69447deba40": ("06_computer_info-20210913-20", 1),
    "8ef8e107-005f-46d5-9b29-d4f6850e37ae": ("06_computer_info-20210913-20", 76),
    "84a169ce-c309-492e-8486-8aaf139d2f1f": ("07_other-20210913-16", 1),
    "310ccbc1-0627-4dab-8541-d7a47b6dce65": ("07_other-20210913-16", 76),
    "171bbe9a-cff8-4ceb-abac-cd9f53f2e7cb": ("07_other-20210913-17", 1),
    "03369a49-300c-4b0a-89eb-a513cf9ed86c": ("07_other-20210913-17", 76),
    "fda6d133-7e39-4d70-9d1e-13a284b574c1": ("07_other-20210913-18", 1),
    "b62785d6-e5d0-4128-a9c4-a97b55d89c63": ("07_other-20210913-18", 76),
    "70c14eae-cc63-41cb-8c03-3490e43b67d2": ("07_other-20210913-19", 1),
    "5244c046-9556-4d4d-a495-d4ec354c5c21": ("07_other-20210913-19", 76),
    "bc12eaf9-3f96-40ca-93a8-a531b3c14cae": ("07_other-20210913-20", 1),
    "fc84be48-136e-4bae-8940-a3954e46c048": ("07_other-20210913-20", 76),
}


def walk_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for value in obj.values():
            yield from walk_strings(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk_strings(value)


def ordered_lines(path: Path) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for text in walk_strings(obj):
            for piece in text.splitlines():
                piece = piece.strip()
                if not LINE.match(piece) or piece in seen:
                    continue
                found.append(piece)
                seen.add(piece)
    return found


def main() -> None:
    chunks: dict[str, dict[int, list[str]]] = defaultdict(dict)
    missing: list[str] = []
    for aid, (book_id, start) in MAP.items():
        path = BASE / f"{aid}.jsonl"
        if not path.exists():
            missing.append(aid)
            continue
        lines = ordered_lines(path)
        bodies: list[str] = []
        for item in lines:
            match = LINE.match(item)
            body = item[match.end() :].strip() if match else item
            if body:
                bodies.append(body)
            if len(bodies) >= 75:
                break
        numbered = [f"{start + i:03d}、{bodies[i]}" for i in range(min(75, len(bodies)))]
        chunks[book_id][start] = numbered
        print(f"seg {book_id} {start} raw={len(lines)} keep={len(numbered)}")
    if missing:
        raise SystemExit(f"missing files: {missing}")
    for book_id in sorted(chunks):
        merged = chunks[book_id].get(1, []) + chunks[book_id].get(76, [])
        cleaned = extract_highlights("\n".join(merged))
        print(
            "BOOK",
            book_id,
            "merged",
            len(merged),
            "extract",
            len(cleaned),
            "keys",
            sorted(chunks[book_id]),
        )
        if len(cleaned) != 150:
            raise SystemExit(f"{book_id} not 150")
        print(write_highlights(ROOT, book_id, cleaned))
    verify()


def verify() -> None:
    from findbook_writer import check_index_link, read_json

    ids = sorted({book_id for book_id, _start in MAP.values()})
    manifest = read_json(ROOT / "data.json")
    total = manifest.get("totalBooks")
    count = len(manifest.get("books") or [])
    if total != count:
        raise SystemExit(f"totalBooks {total} != books {count}")
    for book_id in ids:
        check_index_link(ROOT, book_id)
        row = next(item for item in manifest["books"] if item.get("id") == book_id)
        book = read_json(ROOT / row["file"])
        highlights = book.get("chatgptHighlights") or []
        ok = (
            len(highlights) == 150
            and book.get("chatgptStatus") == "complete"
            and book.get("highlightsSource") == "grok"
            and bool(book.get("highlightsCapturedAt"))
            and str(highlights[0]).startswith("001、")
            and str(highlights[-1]).startswith("150、")
            and book.get("id") == book_id
        )
        print("VERIFY", book_id, "ok" if ok else "FAIL", book.get("title"), len(highlights))
        if not ok:
            raise SystemExit(f"{book_id} status check failed")


if __name__ == "__main__":
    if "verify" in sys.argv:
        verify()
    else:
        main()
