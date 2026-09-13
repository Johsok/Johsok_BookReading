# -*- coding: utf-8 -*-
"""Extract 001-150 lines from this batch's subagent jsonl and write_highlights."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_highlights import write_highlights

ROOT = Path(__file__).resolve().parents[1]
BASE = Path(
    r"C:\Users\johso\.cursor\projects\c-Users-johso-OneDrive-Desktop-Johsok-BookReading"
    r"\agent-transcripts\cbeb487a-dd1b-47a1-b1d2-a50afcf70d89\subagents"
)
LINE_RE = re.compile(r"^(\d{3})、")
PAIR = {
    "01_business_startup-20240913-21": [
        "35a5f99a-99ee-4d13-9295-54830068605e",
        "39130299-da69-484a-a359-dd45121f7b23",
    ],
    "01_business_startup-20240913-22": [
        "25b7004e-6ae9-47c4-857e-dfd6abec225c",
        "3e8dcf98-5c07-4d0a-a2f8-2156d3a5e83f",
    ],
    "01_business_startup-20240913-23": [
        "190e9656-9572-4064-baf2-aea74c69b78b",
        "6bb66209-d6df-4100-b7c1-468715a40941",
    ],
    "01_business_startup-20240913-24": [
        "c361996f-f264-4ebc-9c1a-8e5c3c490894",
        "d00ad98c-0dfc-446d-960f-801a3951e4c2",
    ],
    "01_business_startup-20240913-25": [
        "99663c42-ac71-4563-8d45-70aa98ebef5c",
        "cc665c05-71fb-4771-8a95-2661640aea39",
    ],
    "02_psychology_growth-20240913-21": [
        "ed0c7bb8-091b-4733-af2c-4b39097fa682",
        "4231a53c-6a76-4214-8619-34106bbe9f74",
    ],
    "02_psychology_growth-20240913-22": [
        "039a589b-587d-4f50-98d7-627744af899f",
        "acaafb44-fd4b-4f64-b4b3-8badfb5cc40d",
    ],
    "02_psychology_growth-20240913-23": [
        "4fb1cfbd-9333-4c3d-9903-d90badc6cf8e",
        "0cffcf50-ec92-4358-a0dd-236afa5e94bb",
    ],
    "02_psychology_growth-20240913-24": [
        "f732e6f9-a083-41e9-8893-716929f08a53",
        "32f1a71e-b4f4-4406-9c69-9bec1f985141",
    ],
    "02_psychology_growth-20240913-25": [
        "6d703fc5-fa85-4c8b-a5b7-5834c88bea7f",
        "3d07f3f0-613b-4549-8620-cad0e3e2e6b9",
    ],
    "03_natural_science-20240913-21": [
        "213077e3-d854-4916-a92b-17848612dc2d",
        "6d63058a-b313-4915-9dbb-2773172d7d08",
    ],
    "03_natural_science-20240913-22": [
        "73548b0d-c5b2-4791-8093-590ca0f89ffa",
        "32e3aac9-8e36-45df-9ce5-9d41421dc6a1",
    ],
    "03_natural_science-20240913-23": [
        "baaef089-6b61-4e25-8645-12ce6fb9af1f",
        "e67acbab-e513-4060-9ba4-ae2b1331590d",
    ],
    "03_natural_science-20240913-24": [
        "c896b390-a6a6-45f3-af0c-66c5c2446942",
        "e130138c-1277-4032-a476-d4ca409b73dc",
    ],
    "03_natural_science-20240913-25": [
        "c51bf06b-1773-47b9-8334-ffd9d6d3f859",
        "71887231-5b06-43bf-b426-bdd81e7d04d5",
    ],
    "04_healthcare-20240913-21": [
        "10c078d8-dc02-481d-ae43-51a91adf8482",
        "29b0e026-4919-40cc-a11f-9f948d6aa127",
    ],
    "04_healthcare-20240913-22": [
        "27141201-cc8d-47c5-93a6-17e0bdfb5111",
        "6a5b8bfe-67de-4fc3-ae33-f39f8232276d",
    ],
    "04_healthcare-20240913-23": [
        "5708dfb5-48c5-48c6-9537-53e838f3d0da",
        "dbcf002f-eae0-4f65-811e-03e4139d3653",
    ],
    "04_healthcare-20240913-24": [
        "e754b922-f279-4aa9-a6b2-4516f291877f",
        "4a92464e-0bf8-40d2-a5b5-87ac1cad37dc",
    ],
    "04_healthcare-20240913-25": [
        "73ef91d1-98a6-4316-b915-2a750d01142b",
        "0f306d2f-94ed-417f-b0be-42abb701684b",
    ],
}


def walk_strings(node, out: list[str]) -> None:
    if isinstance(node, str):
        out.append(node)
        return
    if isinstance(node, dict):
        for value in node.values():
            walk_strings(node if False else value, out)
        return
    if isinstance(node, list):
        for item in node:
            walk_strings(item, out)


def harvest(agent_id: str) -> dict[int, str]:
    path = BASE / f"{agent_id}.jsonl"
    found: dict[int, str] = {}
    if not path.is_file():
        return found
    blobs: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        obj = json.loads(raw)
        walk_strings(obj, blobs)
    for blob in blobs:
        for line in blob.replace("\\n", "\n").splitlines():
            line = line.strip().strip('"')
            match = LINE_RE.match(line)
            if not match:
                extra = re.search(r"(\d{3}、.+)$", line)
                if not extra:
                    continue
                line = extra.group(1)
                match = LINE_RE.match(line)
                if not match:
                    continue
            number = int(match.group(1))
            if 1 <= number <= 150 and (number not in found or len(line) > len(found[number])):
                found[number] = line
    return found


def main() -> int:
    for book_id, agent_ids in PAIR.items():
        merged: dict[int, str] = {}
        for agent_id in agent_ids:
            for number, line in harvest(agent_id).items():
                if number not in merged or len(line) > len(merged[number]):
                    merged[number] = line
        missing = [index for index in range(1, 151) if index not in merged]
        print(f"{book_id} got={len(merged)} missing={missing[:12]}")
        if missing:
            continue
        if book_id == "03_natural_science-20240913-23" and 125 in merged:
            merged[125] = merged[125].replace("鎝九十九 hinter", "鎝-99m")
        result = write_highlights(ROOT, book_id, [merged[index] for index in range(1, 151)])
        print("wrote", result)
    import findbook_writer as writer

    manifest = writer.read_json(ROOT / "data.json")
    books = manifest.get("books") or []
    print("totalBooks", manifest.get("totalBooks"), "len", len(books))
    errors: list[str] = []
    for book_id in PAIR:
        try:
            writer.check_index_link(ROOT, book_id)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"link {book_id}: {exc}")
            continue
        matches = [item for item in books if item.get("id") == book_id]
        book = writer.read_json(ROOT / str(matches[0]["file"]))
        highlights = book.get("chatgptHighlights") or []
        garbled = any(
            ("\ufffd" in line or "锟斤拷" in line or "ï¿½" in line or " hinter" in line)
            for line in highlights
        )
        status = book.get("chatgptStatus")
        print(
            f"CHECK {book_id} {status} n={len(highlights)} "
            f"src={book.get('highlightsSource')} garbled={garbled}"
        )
        if status != "complete" or len(highlights) != 150 or garbled:
            errors.append(f"content {book_id}")
        if (
            book.get("id") != book_id
            or book.get("categoryId") != matches[0].get("categoryId")
            or book.get("title") != matches[0].get("title")
            or book.get("author") != matches[0].get("author")
        ):
            errors.append(f"mismatch {book_id}")
    print("errors", len(errors))
    for item in errors:
        print("ERR", item)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
