# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_highlights as hl  # noqa: E402

LINE_RE = re.compile(r"^(\d{3})、")
TRANS = Path(
    r"C:\Users\johso\.cursor\projects\c-Users-johso-OneDrive-Desktop-Johsok-BookReading\agent-transcripts\db71fd72-9b05-4317-afab-45d4b89a97f9\subagents"
)

BOOKS = {
    "05_food_wellness-20210913-21": [
        "3054d89b-10c4-4fc9-9cfe-23bfc3961273",
        "32bd69a0-0926-4e2f-838d-e8ebb5658317",
    ],
    "05_food_wellness-20210913-22": [
        "250d46ec-43ff-45b2-9b9b-3ecf63efd10c",
        "f1bd63d1-ddde-4ce4-87c0-7dcf34738d7b",
    ],
    "05_food_wellness-20210913-23": [
        "95d05a3e-fdf2-447f-9cdf-c130afe46e7a",
        "563833b0-116b-47cf-bca6-02cebc15b9dc",
    ],
    "05_food_wellness-20210913-24": [
        "e59bc606-9c5f-4f0e-9fe8-1d1e34f3c740",
        "17d5ef4c-871d-45d5-a2b9-94c5b1032b2b",
    ],
    "05_food_wellness-20210913-25": [
        "e04ae54e-2d59-4a7c-ba72-fda879c39869",
        "1d231466-7a8e-4f14-8977-db43553c6ec1",
    ],
    "07_other-20210913-21": [
        "b64d7828-e8bb-42a2-859b-29a6ac9bd2cc",
        "11f6150d-a770-416a-99f4-76cc1c876236",
    ],
    "07_other-20210913-22": [
        "96ac69b7-e446-4176-b2c1-89894a306a39",
        "456a0f25-6990-4b27-9c83-a2e669c49b8b",
    ],
    "07_other-20210913-23": [
        "cfe1885e-99ce-4f06-a86c-968a3e8161e8",
        "c16a24b3-1f37-4ae5-8a9c-e680f50d71bd",
    ],
    "07_other-20210913-24": [
        "ff17ae7a-089d-4d12-8346-e7bb528ec568",
        "e21ef580-f792-4098-ad4b-75a49ffefeb0",
    ],
    "07_other-20210913-25": [
        "219ea1b9-6507-46f7-8bc4-dffaaef10f1f",
        "ae443bd1-febe-45ac-9d5d-e6b04803b898",
    ],
    "06_computer_info-20210913-21": [
        "333339f7-d504-4a61-82ff-20627f3c0e43",
        "a4d95b6d-7681-49ed-b393-90be1aedcbfd",
    ],
    "06_computer_info-20210913-22": [
        "73540055-5e4a-4e5b-bd16-afb0b3f43787",
        "2202bee5-9e3b-4820-8ef1-20c0ab2e3a09",
    ],
    "06_computer_info-20210913-23": [
        "e25c7e15-d7d8-449f-9623-3c37ed46415b",
        "329f9f6c-c6d1-4846-9f7e-204016ade30c",
    ],
    "06_computer_info-20210913-24": [
        "f4b294b0-4788-465b-bbc1-5879d7717c58",
        "1c813832-44dd-4cab-bf86-15d0ff9b3dc5",
    ],
    "06_computer_info-20210913-25": [
        "1ac2a2e7-1b71-44cb-9ecc-d673735e804d",
        "4a8f0c0d-b4ae-45d3-9729-f113af8ea6f8",
    ],
}


def extract_lines_from_jsonl(path: Path) -> dict[int, str]:
    found: dict[int, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.startswith("{"):
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if obj.get("role") != "assistant":
            continue
        message = obj.get("message") or {}
        for block in message.get("content") or []:
            if not isinstance(block, dict) or block.get("type") != "text":
                continue
            for line in str(block.get("text") or "").splitlines():
                line = line.strip()
                match = LINE_RE.match(line)
                if not match:
                    continue
                number = int(match.group(1))
                if 1 <= number <= 150:
                    found[number] = line
    return found


def main() -> None:
    for book_id, agent_ids in BOOKS.items():
        merged: dict[int, str] = {}
        for agent_id in agent_ids:
            path = TRANS / f"{agent_id}.jsonl"
            if not path.is_file():
                print("MISSING", book_id, agent_id)
                continue
            merged.update(extract_lines_from_jsonl(path))
        missing = [i for i in range(1, 151) if i not in merged]
        print(book_id, "count", 150 - len(missing), "missing", missing[:8])
        if missing:
            continue
        lines = [merged[i] for i in range(1, 151)]
        result = hl.write_highlights(ROOT, book_id, lines)
        print("written", result)


if __name__ == "__main__":
    main()
