import json
import re
import sys
from pathlib import Path


def extract_highlights(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if re.match(r"^\d{3}、", line):
            lines.append(line)
    return lines


def main() -> None:
    src = Path(sys.argv[1])
    book_id = sys.argv[2]
    out = Path(sys.argv[3])
    highlights = extract_highlights(src.read_text(encoding="utf-8"))
    print(f"{book_id} lines={len(highlights)} first={highlights[0][:20] if highlights else ''} last={highlights[-1][:20] if highlights else ''}")
    out.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
