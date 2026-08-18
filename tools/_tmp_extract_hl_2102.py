# -*- coding: utf-8 -*-
"""Extract Grok 150-point replies from current-session subagents and write books."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import _tmp_write_hl_noguard as hl  # noqa: E402

SUB = (
    Path.home()
    / ".cursor"
    / "projects"
    / "c-Users-johso-OneDrive-Desktop-Johsok-BookReading"
    / "agent-transcripts"
    / "2fdc73db-9546-445c-870a-45803ee46d8e"
    / "subagents"
)

MAP = {
    "576c7408-8dc7-4b84-8d9e-b0c052147344": "01_business_startup-20260818-13",
    "aaffeb9b-6a89-4062-9c16-25c1503e6374": "01_business_startup-20260818-14",
    "d209acb7-0ee5-461f-9f58-e280be2aa712": "01_business_startup-20260818-15",
    "16244ed2-9b2b-4a05-825d-07172156790f": "01_business_startup-20260818-16",
    "ae50a4ef-4693-411c-9c3b-626af8f4e99d": "01_business_startup-20260818-17",
    "2f3cf841-41e6-4733-88e1-400e9da3c1b6": "02_psychology_growth-20260818-13",
    "d339cdef-959f-42ba-81b9-5fef24db5845": "02_psychology_growth-20260818-14",
    "4f29b056-facd-4a0f-8c23-1fac4b00aa72": "02_psychology_growth-20260818-15",
    "62e42d2b-9f54-4487-9e19-da047ca74e9f": "02_psychology_growth-20260818-16",
    "369d67d3-617c-4e82-8705-d3b5de0a912a": "02_psychology_growth-20260818-17",
    "70b46135-5ffb-4746-9650-db18bb88efec": "03_natural_science-20260818-03",
    "293150b4-41c3-4bd7-b290-a459785f30d5": "03_natural_science-20260818-04",
    "2f3cdc82-9e75-4ce0-b7e0-995fb1ea5ba4": "03_natural_science-20260818-05",
    "5b460336-68f1-4832-b424-f3505bf99281": "03_natural_science-20260818-06",
    "dbaa217b-3de5-4c96-a3e1-c837c799ac87": "03_natural_science-20260818-07",
}

LINE_RE = re.compile(r"^\d{3}、")


def extract_text(path: Path) -> str:
    chunks: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            item = json.loads(raw)
        except json.JSONDecodeError:
            continue
        message = item.get("message") or item
        content = message.get("content") if isinstance(message, dict) else None
        if isinstance(content, str):
            chunks.append(content)
            continue
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict):
                    text = part.get("text") or part.get("content") or ""
                    if text:
                        chunks.append(str(text))
                elif isinstance(part, str):
                    chunks.append(part)
        # also scan common keys
        for key in ("text", "output", "response"):
            value = item.get(key)
            if isinstance(value, str) and "001、" in value:
                chunks.append(value)
    return "\n".join(chunks)


def parse_highlights(blob: str) -> list[str]:
    found: dict[int, str] = {}
    for raw in blob.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            continue
        if not LINE_RE.match(line):
            continue
        number = int(line[:3])
        found[number] = line
    return [found[index] for index in range(1, 151) if index in found]


def main() -> int:
    out_dir = ROOT / "tools" / ".hl_2102"
    out_dir.mkdir(exist_ok=True)
    failed = 0
    for agent_id, book_id in MAP.items():
        path = SUB / f"{agent_id}.jsonl"
        blob = extract_text(path)
        highlights = parse_highlights(blob)
        txt = out_dir / f"{book_id}.txt"
        txt.write_text("\n".join(highlights) + "\n", encoding="utf-8")
        print(f"extract\t{book_id}\t{len(highlights)}\t{path.exists()}")
        if not highlights:
            failed += 1
            continue
        sys.argv = ["_tmp_write_hl_noguard.py", book_id, str(txt)]
        hl.main()
    if failed:
        raise SystemExit(f"empty highlights for {failed} books")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
